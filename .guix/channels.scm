;; 工具链唯一真相源。
;; 由 `guix describe -f channels` 生成后手工裁剪：只保留 guix 频道。
;; 改这里等于改全书的构建环境，属于受保护变更。
(list (channel
        (name 'guix)
        (url "https://git.guix.gnu.org/guix.git")
        (branch "master")
        (commit "728b1b8bf6744d538382f69325008829488f2b30")
        (introduction
          (make-channel-introduction
            "9edb3f66fd807b096b48283debdcddccfea34bad"
            (openpgp-fingerprint
              "BBB0 2DDF 2CEA F6A8 0D1D  E643 A2A0 6DF2 A33A 54FA")))))
