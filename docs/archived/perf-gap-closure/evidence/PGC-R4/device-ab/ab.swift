import Metal
import Foundation

// PGC-R4 device A/B: old-recipe MSL (R3 evidence) vs new simdgroup MSL
// (this branch's export), same seeded inputs, per-family tolerance record.
let oldDir = "/Users/ianzepp/work/faberlang/worktrees/pgc-b2/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-raw/parity-metal-m5max-fixed1000/gea3-export/artifacts"
let newDir = "/tmp/r4-art/d"
let family: [(String, UInt32, UInt32, UInt32)] = [
    ("prefill_gemm_qo", 36, 960, 960),
    ("prefill_gemm_kv", 36, 960, 320),
    ("prefill_gemm_gate_up", 36, 960, 2560),
    ("prefill_gemm_down", 36, 2560, 960),
    ("prefill_gemm_o", 36, 960, 960),
]

func lcg(_ count: Int) -> [Float] {
    var next: UInt64 = 0x2545_F491_4F6C_DD1D
    var out = [Float](); out.reserveCapacity(count)
    for _ in 0..<count {
        next = next &* 6_364_136_223_846_793_005 &+ 1_442_695_040_888_963_407
        out.append(Float(Int32(truncatingIfNeeded: next >> 33)) / Float(1 << 31))
    }
    return out
}

guard let dev = MTLCreateSystemDefaultDevice() else { fatalError("no device") }
func makePS(_ path: String) -> MTLComputePipelineState {
    let src = try! String(contentsOfFile: path, encoding: .utf8)
    let sem = DispatchSemaphore(value: 0)
    var lib: MTLLibrary? = nil; var err: Error? = nil
    dev.makeLibrary(source: src, options: nil) { l, e in lib = l; err = e; sem.signal() }
    sem.wait()
    if let e = err { fatalError("compile \(path): \(e)") }
    return try! dev.makeComputePipelineState(function: lib!.makeFunction(name: (path as NSString).lastPathComponent.replacingOccurrences(of: ".metal", with: ""))!)
}

func runKernel(_ ps: MTLComputePipelineState, _ A: [Float], _ B: [Float], m: Int, k: Int, n: Int) -> [Float] {
    let ab = dev.makeBuffer(bytes: A, length: A.count*4)!
    let bb = dev.makeBuffer(bytes: B, length: B.count*4)!
    let e0 = dev.makeBuffer(length: 4)!, e1 = dev.makeBuffer(length: 4)!
    let cb = dev.makeBuffer(length: m*n*4)!
    let q = dev.makeCommandQueue()!
    let cmd = q.makeCommandBuffer()!
    let enc = cmd.makeComputeCommandEncoder()!
    enc.setComputePipelineState(ps)
    enc.setBuffer(ab, offset: 0, index: 0)
    enc.setBuffer(bb, offset: 0, index: 1)
    enc.setBuffer(e0, offset: 0, index: 2)
    enc.setBuffer(e1, offset: 0, index: 3)
    enc.setBuffer(cb, offset: 0, index: 4)
    enc.dispatchThreadgroups(MTLSize(width: (n+7)/8, height: (m+7)/8, depth: 1),
                             threadsPerThreadgroup: MTLSize(width: 8, height: 8, depth: 1))
    enc.endEncoding()
    cmd.commit(); cmd.waitUntilCompleted()
    return Array(UnsafeBufferPointer(start: cb.contents().assumingMemoryBound(to: Float.self), count: m*n))
}

var record: [String: Any] = [
    "schema": "pgc-r4-frozen-tolerance-v1",
    "device": dev.name,
    "seed": "lcg 0x2545F4914F6CDD1D",
    "note": "class B: simdgroup accumulate contracts the multiply-add; frozen per-family bounds vs CPU reference and vs the old (R3) recipe output; never widened",
]
var perFamily: [String: Any] = [:]
for (entry, m, k, n) in family {
    let A = lcg(Int(m)*Int(k))
    let B = lcg(Int(n)*Int(k))
    var ref = [Float](repeating: 0, count: Int(m)*Int(n))
    for r in 0..<Int(m) { for c in 0..<Int(n) {
        var s: Float = 0
        for i in 0..<Int(k) { s += A[r*Int(k)+i] * B[c*Int(k)+i] }
        ref[r*Int(n)+c] = s
    }}
    let oldPS = makePS("\(oldDir)/\(entry).metal")
    let newPS = makePS("\(newDir)/\(entry).metal")
    let oldOut = runKernel(oldPS, A, B, m: Int(m), k: Int(k), n: Int(n))
    let newOut = runKernel(newPS, A, B, m: Int(m), k: Int(k), n: Int(n))
    var maxOldCPU: Float = 0, maxNewCPU: Float = 0, maxNewOld: Float = 0, maxRelCPU: Float = 0
    var sigBitsOld = 0, sigBitsNewOld = 0
    for i in 0..<(Int(m)*Int(n)) {
        maxOldCPU = max(maxOldCPU, abs(ref[i]-oldOut[i]))
        maxNewCPU = max(maxNewCPU, abs(ref[i]-newOut[i]))
        maxNewOld = max(maxNewOld, abs(newOut[i]-oldOut[i]))
        maxRelCPU = max(maxRelCPU, abs(ref[i]-newOut[i]) / max(abs(ref[i]), 1e-3))
        let bitsOld = ref[i].bitPattern ^ oldOut[i].bitPattern
        sigBitsOld = max(sigBitsOld, bitsOld.leadingZeroBitCount < 32 ? 32 - bitsOld.leadingZeroBitCount : 0)
        let bitsNewOld = oldOut[i].bitPattern ^ newOut[i].bitPattern
        sigBitsNewOld = max(sigBitsNewOld, bitsNewOld.leadingZeroBitCount < 32 ? 32 - bitsNewOld.leadingZeroBitCount : 0)
    }
    perFamily[entry] = [
        "m": m, "k": k, "n": n,
        "old_max_abs_vs_cpu": maxOldCPU,
        "max_abs_vs_cpu": maxNewCPU,
        "max_rel_vs_cpu": maxRelCPU,
        "max_abs_vs_old": maxNewOld,
        "max_differing_mantissa_bits_vs_cpu": sigBitsOld,
        "max_differing_mantissa_bits_vs_old": sigBitsNewOld,
    ] as [String: Any]
    print("\(entry): old-vs-cpu=\(maxOldCPU) new-vs-cpu=\(maxNewCPU) new-vs-old=\(maxNewOld) rel=\(maxRelCPU)")
}
record["families"] = perFamily
let json = try! JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys])
try! json.write(to: URL(fileURLWithPath: "/tmp/r4-ab.json"))
print("WROTE /tmp/r4-ab.json")
