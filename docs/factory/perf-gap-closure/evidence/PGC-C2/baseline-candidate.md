{
  "blocks": [
    {
      "gradus_tps": {
        "decode": {
          "max": 32.867437,
          "median": 31.657466,
          "min": 29.743426,
          "runs": 3,
          "status": "measured",
          "value": 31.657466
        },
        "prefill": {
          "max": 578.229654,
          "median": 554.289586,
          "min": 473.148805,
          "runs": 3,
          "status": "measured",
          "value": 554.289586
        }
      },
      "llama_tps": {
        "decode": {
          "max": 212.089077,
          "median": 205.338809,
          "min": 172.935581,
          "runs": 3,
          "status": "measured",
          "value": 205.338809
        },
        "prefill": {
          "max": 1520.912548,
          "median": 1284.796574,
          "min": 898.652022,
          "runs": 3,
          "status": "measured",
          "value": 1284.796574
        }
      },
      "power_class": "ac",
      "ratio": {
        "decode": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 6.486268,
          "status": "measured",
          "value": 6.486268
        },
        "prefill": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 2.317916,
          "status": "measured",
          "value": 2.317916
        }
      },
      "rows": [
        {
          "arms": {
            "gradus": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 268.967,
                  "tokens": 8,
                  "ts": 29.743426,
                  "value": 29.743426
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 76.086,
                  "tokens": 36,
                  "ts": 473.148805,
                  "value": 473.148805
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 46.26,
                  "tokens": 8,
                  "ts": 172.935581,
                  "value": 172.935581
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 40.06,
                  "tokens": 36,
                  "ts": 898.652022,
                  "value": 898.652022
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 5.814246
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 1.899301
            }
          },
          "run": 1,
          "status": "comparable"
        },
        {
          "arms": {
            "gradus": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 252.705,
                  "tokens": 8,
                  "ts": 31.657466,
                  "value": 31.657466
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 64.948,
                  "tokens": 36,
                  "ts": 554.289586,
                  "value": 554.289586
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 38.96,
                  "tokens": 8,
                  "ts": 205.338809,
                  "value": 205.338809
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 23.67,
                  "tokens": 36,
                  "ts": 1520.912548,
                  "value": 1520.912548
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 6.486268
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 2.743895
            }
          },
          "run": 2,
          "status": "comparable"
        },
        {
          "arms": {
            "gradus": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 243.402,
                  "tokens": 8,
                  "ts": 32.867437,
                  "value": 32.867437
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 62.259,
                  "tokens": 36,
                  "ts": 578.229654,
                  "value": 578.229654
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 8,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 37.72,
                  "tokens": 8,
                  "ts": 212.089077,
                  "value": 212.089077
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 28.02,
                  "tokens": 36,
                  "ts": 1284.796574,
                  "value": 1284.796574
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 6.452863
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 2.221949
            }
          },
          "run": 3,
          "status": "comparable"
        }
      ],
      "runs": 3,
      "status": "comparable",
      "test": "metal-m5max"
    },
    {
      "gradus_tps": {
        "decode": {
          "max": 16.048561,
          "median": 15.938926,
          "min": 15.456944,
          "runs": 3,
          "status": "measured",
          "value": 15.938926
        },
        "prefill": {
          "max": 562.719812,
          "median": 535.109103,
          "min": 530.121192,
          "runs": 3,
          "status": "measured",
          "value": 535.109103
        }
      },
      "llama_tps": {
        "decode": {
          "max": 254.048904,
          "median": 224.794875,
          "min": 210.592819,
          "runs": 3,
          "status": "measured",
          "value": 224.794875
        },
        "prefill": {
          "max": 3225.806452,
          "median": 1926.163724,
          "min": 1909.814324,
          "runs": 3,
          "status": "measured",
          "value": 1926.163724
        }
      },
      "power_class": "ac",
      "ratio": {
        "decode": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 14.103515,
          "status": "measured",
          "value": 14.103515
        },
        "prefill": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 3.599572,
          "status": "measured",
          "value": 3.599572
        }
      },
      "rows": [
        {
          "arms": {
            "gradus": {
              "certified_count": 1000,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 62739.483,
                  "tokens": 1000,
                  "ts": 15.938926,
                  "value": 15.938926
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 67.909,
                  "tokens": 36,
                  "ts": 530.121192,
                  "value": 530.121192
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 40,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 157.45,
                  "tokens": 40,
                  "ts": 254.048904,
                  "value": 254.048904
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 11.16,
                  "tokens": 36,
                  "ts": 3225.806452,
                  "value": 3225.806452
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 15.938897
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 6.085036
            }
          },
          "run": 1,
          "status": "comparable"
        },
        {
          "arms": {
            "gradus": {
              "certified_count": 1000,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 64695.843,
                  "tokens": 1000,
                  "ts": 15.456944,
                  "value": 15.456944
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 63.975,
                  "tokens": 36,
                  "ts": 562.719812,
                  "value": 562.719812
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 40,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 189.94,
                  "tokens": 40,
                  "ts": 210.592819,
                  "value": 210.592819
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 18.85,
                  "tokens": 36,
                  "ts": 1909.814324,
                  "value": 1909.814324
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 13.62448
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 3.393899
            }
          },
          "run": 2,
          "status": "comparable"
        },
        {
          "arms": {
            "gradus": {
              "certified_count": 1000,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "sum of this arm's measured GEA3 per-step decode walls over its certified count",
                  "status": "measured",
                  "time_ms": 62310.881,
                  "tokens": 1000,
                  "ts": 16.048561,
                  "value": 16.048561
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 67.276,
                  "tokens": 36,
                  "ts": 535.109103,
                  "value": 535.109103
                }
              },
              "status": "measured"
            },
            "llama": {
              "certified_count": 40,
              "completion_status": "natural_completion",
              "count_certified": true,
              "phases": {
                "decode": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 177.94,
                  "tokens": 40,
                  "ts": 224.794875,
                  "value": 224.794875
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 18.69,
                  "tokens": 36,
                  "ts": 1926.163724,
                  "value": 1926.163724
                }
              },
              "status": "measured"
            }
          },
          "power_class": "ac",
          "ratio": {
            "decode": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 14.007167
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 3.599572
            }
          },
          "run": 3,
          "status": "comparable"
        }
      ],
      "runs": 3,
      "status": "comparable",
      "test": "metal-m5max-fixed1000"
    }
  ],
  "created_utc": "2026-08-27T22:01:22Z",
  "identities": {
    "metal-m5max": {
      "cap_seconds": 60,
      "comparator": {
        "binary": "/Users/ianzepp/work/llama.cpp/build-gea1-c8e03ce81/bin/llama-cli",
        "build": "b10290-c8e03ce81",
        "generation_flags": [
          "-n",
          "8",
          "--seed",
          "0",
          "--temp",
          "0",
          "--top-k",
          "1",
          "--top-p",
          "1",
          "--no-display-prompt",
          "--no-conversation",
          "--single-turn",
          "--verbose-prompt",
          "--log-verbosity",
          "3"
        ],
        "sha256": "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
      },
      "expected_tokens": {
        "comparator": 8,
        "faber": 8,
        "law": "46ab4e94"
      },
      "gguf": {
        "bytes": 1449071552,
        "file": "SmolLM2-360M-Instruct-f32.gguf",
        "sha256": "4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128",
        "subpath": "derived/HuggingFaceTB/SmolLM2-360M-Instruct/a10cc1512eabd3dde888204e902eca88bddb4951/SmolLM2-360M-Instruct-f32.gguf",
        "tensor_bytes": 1447284480,
        "tensor_values": 361821120,
        "tensors": 290
      },
      "gradus": {
        "kernel_sha256": "57345d456ab45a0a5e4019c586aa22d8867541909df68285120bd0be463da187",
        "kernel_source": "src/kernel.fab",
        "revision": "de687a4d2f386a8f30be72d76cec108f434195a9"
      },
      "machine": {
        "backend": "metal",
        "device": "Apple M5 Max, one virtual partition",
        "hostname": "burgus.local"
      },
      "policy": {
        "gea3_input_manifest": "docs/factory/gpu-execution-architecture/evidence/gea3-input-manifest.json",
        "kv_bytes": 6225920,
        "l_max": 76,
        "l_max_formula": "prompt(36) + n_predict(8) + margin(32)",
        "n_predict": 8,
        "sampling": "greedy argmax, first-index tie",
        "seed": 0
      },
      "prompt": {
        "comparator_token_ids": [
          1,
          9690,
          198,
          2683,
          359,
          253,
          5356,
          5646,
          11173,
          3365,
          3511,
          308,
          34519,
          28,
          7018,
          411,
          407,
          19712,
          8182,
          2,
          198,
          1,
          4093,
          198,
          504,
          31469,
          6740,
          335,
          2591,
          314,
          2,
          198,
          1,
          520,
          9531,
          198
        ],
        "effective_tokens": 36,
        "sha256": "0a8c8e2698356927060027ef2e30648a63f0c31ff869c7f14f64f4a1fbf939ea",
        "text": "The tallest mountain on Earth is"
      },
      "target_id": "metal-m5max",
      "termination_tolerance_seconds": 70,
      "warmup_exclusion_rule": "Unchanged from the existing KV F5 harness rule: the first 16 decode steps are warmup and are discarded before the measured window (16 warmup + 128 measured stays frozen); startup, plan admission, weight residency, KV allocation, and teardown stay outside steady-state rates. The frozen short identity (n_predict = 8, l_max = 76) is byte-frozen and is never padded, extended, looped, or relaunched to fill a warmup or measurement window."
    },
    "metal-m5max-fixed1000": {
      "cap_seconds": 300,
      "comparator": {
        "binary": "/Users/ianzepp/work/llama.cpp/build-gea1-c8e03ce81/bin/llama-cli",
        "build": "b10290-c8e03ce81",
        "generation_flags": [
          "-n",
          "1000",
          "--seed",
          "0",
          "--temp",
          "0",
          "--top-k",
          "1",
          "--top-p",
          "1",
          "--no-display-prompt",
          "--no-conversation",
          "--single-turn",
          "--verbose-prompt",
          "--log-verbosity",
          "3"
        ],
        "sha256": "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
      },
      "expected_tokens": {
        "comparator": 1000,
        "faber": 1000,
        "law": "46ab4e94"
      },
      "gguf": {
        "bytes": 1449071552,
        "file": "SmolLM2-360M-Instruct-f32.gguf",
        "sha256": "4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128",
        "subpath": "derived/HuggingFaceTB/SmolLM2-360M-Instruct/a10cc1512eabd3dde888204e902eca88bddb4951/SmolLM2-360M-Instruct-f32.gguf",
        "tensor_bytes": 1447284480,
        "tensor_values": 361821120,
        "tensors": 290
      },
      "gradus": {
        "kernel_sha256": "57345d456ab45a0a5e4019c586aa22d8867541909df68285120bd0be463da187",
        "kernel_source": "src/kernel.fab",
        "revision": "de687a4d2f386a8f30be72d76cec108f434195a9"
      },
      "machine": {
        "backend": "metal",
        "device": "Apple M5 Max, one virtual partition",
        "hostname": "burgus.local"
      },
      "policy": {
        "gea3_input_manifest": "docs/factory/gpu-execution-architecture/evidence/gea3-input-manifest.json",
        "kv_bytes": 90112000,
        "l_max": 1100,
        "l_max_formula": "prompt(36) + n_predict(1000) + margin(64)",
        "n_predict": 1000,
        "sampling": "greedy argmax, first-index tie",
        "seed": 0
      },
      "prompt": {
        "comparator_token_ids": [
          1,
          9690,
          198,
          2683,
          359,
          253,
          5356,
          5646,
          11173,
          3365,
          3511,
          308,
          34519,
          28,
          7018,
          411,
          407,
          19712,
          8182,
          2,
          198,
          1,
          4093,
          198,
          504,
          31469,
          6740,
          335,
          2591,
          314,
          2,
          198,
          1,
          520,
          9531,
          198
        ],
        "effective_tokens": 36,
        "sha256": "0a8c8e2698356927060027ef2e30648a63f0c31ff869c7f14f64f4a1fbf939ea",
        "text": "The tallest mountain on Earth is"
      },
      "target_id": "metal-m5max-fixed1000",
      "termination_tolerance_seconds": 310,
      "warmup_exclusion_rule": "Startup, plan admission, weight residency, KV allocation (85.4 MiB fixed F32 reservation), and teardown stay outside steady-state rates; fixed-output-length generation may naturally complete before the 300s hard cap and is never padded, extended, looped, or relaunched to fill a window."
    }
  },
  "provenance": {
    "comparator": {
      "build": "b10290-c8e03ce81",
      "path": "/Users/ianzepp/work/llama.cpp/build-gea1-c8e03ce81/bin/llama-cli",
      "sha256": "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
    },
    "gradus": {
      "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/gradus",
      "revision": "de687a4d2f386a8f30be72d76cec108f434195a9"
    },
    "hosts": {
      "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/hosts",
      "revision": "aaf935db338e62499c358fc73da6c2fb55134cd1"
    },
    "law": "identity and raw-byte validation precede all timing parsing and ratio arithmetic",
    "pins": [
      {
        "comparator": {
          "build": "b10290-c8e03ce81",
          "path": "/Users/ianzepp/work/llama.cpp/build-gea1-c8e03ce81/bin/llama-cli",
          "sha256": "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
        },
        "gguf_sha256": "4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128",
        "gradus": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/gradus",
          "revision": "de687a4d2f386a8f30be72d76cec108f434195a9"
        },
        "hosts": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/hosts",
          "revision": "aaf935db338e62499c358fc73da6c2fb55134cd1"
        },
        "radix": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/radix",
          "revision": "f65d7554db8eb80519a7fc953e243ef5f542ac0b"
        }
      },
      {
        "comparator": {
          "build": "b10290-c8e03ce81",
          "path": "/Users/ianzepp/work/llama.cpp/build-gea1-c8e03ce81/bin/llama-cli",
          "sha256": "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
        },
        "gguf_sha256": "4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128",
        "gradus": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/gradus",
          "revision": "de687a4d2f386a8f30be72d76cec108f434195a9"
        },
        "hosts": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/hosts",
          "revision": "aaf935db338e62499c358fc73da6c2fb55134cd1"
        },
        "radix": {
          "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/radix",
          "revision": "f65d7554db8eb80519a7fc953e243ef5f542ac0b"
        }
      }
    ],
    "radix": {
      "repo": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/radix",
      "revision": "f65d7554db8eb80519a7fc953e243ef5f542ac0b"
    }
  },
  "report": {
    "metric": "tokens per second",
    "no_threshold_gate": true,
    "phases": [
      "prefill",
      "decode"
    ],
    "ratio": "llama t/s / gradus t/s per phase and per power class"
  },
  "schema": "parity-receipt-v1",
  "source": {
    "baseline_grade": true,
    "driver_schema": "parity-driver-v1",
    "protocol": {
      "aggregation": "median across paired runs",
      "baseline_grade": true,
      "breadth": 2,
      "cap_rule": "hard cap per arm; circuit breaker only; never a metric or token target",
      "execution_rule": "on-device Metal arms only; MIR runner excluded",
      "paired_runs": 3,
      "schema": "parity-stage-protocol-v1",
      "stage": "full",
      "stage_number": 4,
      "target_ids": [
        "metal-m5max",
        "metal-m5max-fixed1000"
      ]
    },
    "raw_capture": "/Users/ianzepp/work/faberlang/worktrees/pgc-c2/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-raw",
    "stage": "full",
    "stage_number": 4,
    "tests": [
      "metal-m5max",
      "metal-m5max-fixed1000"
    ]
  }
}
