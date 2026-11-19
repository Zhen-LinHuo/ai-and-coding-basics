# AGENTS.local.md

本仓库的身份与签名。**只用这一把键署名。**

| 项 | 值 |
|:--|:--|
| user.name | Zhen-Lin Huo |
| user.email | zhen-lin.huo@gmx.com |
| user.signingkey | B0F3115E1443673010CE91647C403CA2E7B6861C |
| commit.gpgsign | true |
| tag.gpgsign | true |

## 为什么签名键写指纹而不写名字

本机有两把私钥的 UID 都含 `Zhen-Lin Huo`（另一把属于作者在别处使用的身份，
与本仓库无关，此处不写其邮箱——公开仓库不承担身份关联的义务）。
`gpg --local-user "Zhen-Lin Huo"` 会因两个 UID 都能匹配而报 ambiguous，
所以 `user.signingkey` 必须写完整指纹。

## 远端

`https://github.com/zhen-linhuo/ai-and-coding-basics`（公开仓库）
