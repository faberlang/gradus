{
  "blocks": [
    {
      "gradus_tps": {
        "decode": {
          "max": 37.451255,
          "median": 36.404674,
          "min": 31.928862,
          "runs": 3,
          "status": "measured",
          "value": 36.404674
        },
        "prefill": {
          "max": 562.886985,
          "median": 540.613596,
          "min": 499.271895,
          "runs": 3,
          "status": "measured",
          "value": 540.613596
        }
      },
      "llama_tps": {
        "decode": {
          "max": 209.698558,
          "median": 189.933523,
          "min": 184.119678,
          "runs": 3,
          "status": "measured",
          "value": 189.933523
        },
        "prefill": {
          "max": 1649.106734,
          "median": 1303.403331,
          "min": 1087.284808,
          "runs": 3,
          "status": "measured",
          "value": 1303.403331
        }
      },
      "power_class": "ac",
      "ratio": {
        "decode": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 5.217284,
          "status": "measured",
          "value": 5.217284
        },
        "prefill": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 2.41097,
          "status": "measured",
          "value": 2.41097
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
                  "time_ms": 213.611,
                  "tokens": 8,
                  "ts": 37.451255,
                  "value": 37.451255
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 63.956,
                  "tokens": 36,
                  "ts": 562.886985,
                  "value": 562.886985
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
                  "time_ms": 38.15,
                  "tokens": 8,
                  "ts": 209.698558,
                  "value": 209.698558
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 21.83,
                  "tokens": 36,
                  "ts": 1649.106734,
                  "value": 1649.106734
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
              "value": 5.59924
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 2.92973
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
                  "time_ms": 250.557,
                  "tokens": 8,
                  "ts": 31.928862,
                  "value": 31.928862
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 72.105,
                  "tokens": 36,
                  "ts": 499.271895,
                  "value": 499.271895
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
                  "time_ms": 43.45,
                  "tokens": 8,
                  "ts": 184.119678,
                  "value": 184.119678
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 27.62,
                  "tokens": 36,
                  "ts": 1303.403331,
                  "value": 1303.403331
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
              "value": 5.766559
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 2.610608
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
                  "time_ms": 219.752,
                  "tokens": 8,
                  "ts": 36.404674,
                  "value": 36.404674
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 66.591,
                  "tokens": 36,
                  "ts": 540.613596,
                  "value": 540.613596
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
                  "time_ms": 42.12,
                  "tokens": 8,
                  "ts": 189.933523,
                  "value": 189.933523
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 33.11,
                  "tokens": 36,
                  "ts": 1087.284808,
                  "value": 1087.284808
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
              "value": 5.217284
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 2.011205
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
          "max": 16.472109,
          "median": 16.127834,
          "min": 15.131834,
          "runs": 3,
          "status": "measured",
          "value": 16.127834
        },
        "prefill": {
          "max": 569.395018,
          "median": 447.238303,
          "min": 434.038244,
          "runs": 3,
          "status": "measured",
          "value": 447.238303
        }
      },
      "llama_tps": {
        "decode": {
          "max": 244.498778,
          "median": 240.067219,
          "min": 236.994905,
          "runs": 3,
          "status": "measured",
          "value": 240.067219
        },
        "prefill": {
          "max": 3263.825929,
          "median": 3220.035778,
          "min": 3211.418376,
          "runs": 3,
          "status": "measured",
          "value": 3220.035778
        }
      },
      "power_class": "ac",
      "ratio": {
        "decode": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 14.885273,
          "status": "measured",
          "value": 14.885273
        },
        "prefill": {
          "basis": "llama median t/s / gradus median t/s",
          "median": 7.199821,
          "status": "measured",
          "value": 7.199821
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
                  "time_ms": 66085.844,
                  "tokens": 1000,
                  "ts": 15.131834,
                  "value": 15.131834
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 80.494,
                  "tokens": 36,
                  "ts": 447.238303,
                  "value": 447.238303
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
                  "time_ms": 168.78,
                  "tokens": 40,
                  "ts": 236.994905,
                  "value": 236.994905
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 11.21,
                  "tokens": 36,
                  "ts": 3211.418376,
                  "value": 3211.418376
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
              "value": 15.662008
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 7.180553
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
                  "time_ms": 60708.681,
                  "tokens": 1000,
                  "ts": 16.472109,
                  "value": 16.472109
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 82.942,
                  "tokens": 36,
                  "ts": 434.038244,
                  "value": 434.038244
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
                  "time_ms": 163.6,
                  "tokens": 40,
                  "ts": 244.498778,
                  "value": 244.498778
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 11.03,
                  "tokens": 36,
                  "ts": 3263.825929,
                  "value": 3263.825929
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
              "value": 14.843198
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 7.519674
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
                  "time_ms": 62004.606,
                  "tokens": 1000,
                  "ts": 16.127834,
                  "value": 16.127834
                },
                "prefill": {
                  "basis": "GEA3 execution.prefill_wall_us over the effective prompt tokens",
                  "status": "measured",
                  "time_ms": 63.225,
                  "tokens": 36,
                  "ts": 569.395018,
                  "value": 569.395018
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
                  "time_ms": 166.62,
                  "tokens": 40,
                  "ts": 240.067219,
                  "value": 240.067219
                },
                "prefill": {
                  "basis": "llama-cli stable timing line; decode count is this arm's certified count",
                  "status": "measured",
                  "time_ms": 11.18,
                  "tokens": 36,
                  "ts": 3220.035778,
                  "value": 3220.035778
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
              "value": 14.885273
            },
            "prefill": {
              "basis": "llama t/s divided by gradus t/s, each on its own certified count and phase wall",
              "status": "measured",
              "value": 5.655188
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
  "created_utc": "2026-08-28T06:45:13Z",
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
        "kernel_sha256": "c9cdbb54e5bd35f0dec076f63bb67a289aae71e014360a2550d470a96bf2e08c",
        "kernel_source": "src/kernel.fab",
        "revision": "b762163664b65fcb3d8d71aee23b181ecdd3a1f6"
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
        "kernel_sha256": "c9cdbb54e5bd35f0dec076f63bb67a289aae71e014360a2550d470a96bf2e08c",
        "kernel_source": "src/kernel.fab",
        "revision": "b762163664b65fcb3d8d71aee23b181ecdd3a1f6"
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
      "repo": "/Users/ianzepp/work/faberlang/gradus",
      "revision": "b762163664b65fcb3d8d71aee23b181ecdd3a1f6"
    },
    "hosts": {
      "repo": "/Users/ianzepp/work/faberlang/hosts",
      "revision": "848a24b362eb3c24d741edefda92532a190834ed"
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
          "repo": "/Users/ianzepp/work/faberlang/gradus",
          "revision": "b762163664b65fcb3d8d71aee23b181ecdd3a1f6"
        },
        "hosts": {
          "repo": "/Users/ianzepp/work/faberlang/hosts",
          "revision": "848a24b362eb3c24d741edefda92532a190834ed"
        },
        "radix": {
          "repo": "/Users/ianzepp/work/faberlang/radix",
          "revision": "783e0b91b530c7721caaa8bc36b7b2576cd0b6b1"
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
          "repo": "/Users/ianzepp/work/faberlang/gradus",
          "revision": "b762163664b65fcb3d8d71aee23b181ecdd3a1f6"
        },
        "hosts": {
          "repo": "/Users/ianzepp/work/faberlang/hosts",
          "revision": "848a24b362eb3c24d741edefda92532a190834ed"
        },
        "radix": {
          "repo": "/Users/ianzepp/work/faberlang/radix",
          "revision": "783e0b91b530c7721caaa8bc36b7b2576cd0b6b1"
        }
      }
    ],
    "radix": {
      "repo": "/Users/ianzepp/work/faberlang/radix",
      "revision": "783e0b91b530c7721caaa8bc36b7b2576cd0b6b1"
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
    "raw_capture": "/Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-raw-ac",
    "stage": "full",
    "stage_number": 4,
    "tests": [
      "metal-m5max",
      "metal-m5max-fixed1000"
    ]
  }
}
