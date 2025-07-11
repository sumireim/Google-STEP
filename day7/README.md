# Malloc Challenge Homework 
## Cポインタ百ます計算
![プリント](./malo2.jpg)


## Best-fit mallocに改造
元々、必要なメモリを満たすフリーブロックの中で最初のものを取ってきていたが、必要なメモリを満たすフリーブロックの中で最小のものを取得するように変更した。

その過程で、First Fit, Best Fit, Worst Fitの3つを実装し、それぞれの性能について考察した。
### first-fit
- フリーリストを前から順に走査し、必要なサイズ以上の最初に見つかったブロックを選択
- 利点
  - 時間計算量が小さい
- 欠点
  - 大きいブロックを使用してしまった際に空間効率が悪くなってしまう


| Challenge | 項目 | simple_malloc | my_malloc |
|-----------|------|---------------|-----------|
| **#1** | Time [ms] | 11 | 9 |
|        | Utilization [%] | 70 | 70 |
| **#2** | Time [ms] | 7 | 7 |
|        | Utilization [%] | 40 | 40 |
| **#3** | Time [ms] | 131 | 128 |
|        | Utilization [%] | 9 | 9 |
| **#4** | Time [ms] | 16236 | 17622 |
|        | Utilization [%] | 15 | 15 |
| **#5** | Time [ms] | 14494 | 15497 |
|        | Utilization [%] | 15 | 15 |



### best-fit
- フリーリストを全て走査し、必要なサイズ以上で最もサイズが小さいブロックを選択
- 利点
  - 空間効率が良く無駄が少ない
- 欠点
  - 全てを走査する必要があるので、時間計算量が大きい

| Challenge | 項目 | simple_malloc | my_malloc |
|-----------|------|---------------|-----------|
| **#1** | Time [ms] | 12 | 1581 |
|        | Utilization [%] | 70 | 70 |
| **#2** | Time [ms] | 6 | 1127 |
|        | Utilization [%] | 40 | 40 |
| **#3** | Time [ms] | 128 | 1339 |
|        | Utilization [%] | 9 | 51 |
| **#4** | Time [ms] | 16817 | 9530 |
|        | Utilization [%] | 15 | 72 |
| **#5** | Time [ms] | 10941 | 6126 |
|        | Utilization [%] | 15 | 75 |



### worst-fit
- フリーリストを全て走査し、必要なサイズ以上で最もサイズが大きいブロックを選択
- 利点
  - ?
- 欠点
  - 全てを走査する必要があるので、時間計算量が大きい
  - 空間効率が悪い


| Challenge | 項目 | simple_malloc | my_malloc |
|-----------|------|---------------|-----------|
| **#1** | Time [ms] | 11 | 1592 |
|        | Utilization [%] | 70 | 70 |
| **#2** | Time [ms] | 7 | 1171 |
|        | Utilization [%] | 40 | 40 |
| **#3** | Time [ms] | 129 | 72232 |
|        | Utilization [%] | 9 | 4 |
| **#4** | Time [ms] | 15572 | 773897 |
|        | Utilization [%] | 15 | 7 |
| **#5** | Time [ms] | 9984 | 616437 |
|        | Utilization [%] | 15 | 7 |



## Freelist binを実装

### binの分割方法
8つのbinを作成し、メモリブロックサイズに応じて分類することで、メモリ割り当ての効率を向上を図った。

サイズは8の倍数であることが保証されているので、`multiple_size = size / 8`として正規化してから分類した。

| bin番号 | サイズ範囲 (bytes) | multiple_size範囲 |
|---------|-------------------|-------------------|
| bin[0] | 8 - 32 | 1 - 4 |
| bin[1] | 40 - 64 | 5 - 8 |
| bin[2] | 72 - 128 | 9 - 16 |
| bin[3] | 136 - 256 | 17 - 32 |
| bin[4] | 264 - 512 | 33 - 64 |
| bin[5] | 520 - 1024 | 65 - 128 |
| bin[6] | 1032 - 2048 | 129 - 256 |
| bin[7] | 2056 - 4000+ | 257+ |

初めは、上記のように分類したが、各binに分類されたmalloc要求をprintfした結果、以下のようになった。

| bin番号 | 要求回数 | 割合 | サイズ範囲 (bytes) |
|---------|----------|------|-------------------|
| bin[0] | 418,582 | 34.5% | 8 - 32 |
| bin[1] | 66,121 | 5.4% | 40 - 64 |
| bin[2] | 265,971 | 21.9% | 72 - 128 |
| bin[3] | 39,005 | 3.2% | 136 - 256 |
| bin[4] | 131,690 | 10.8% | 264 - 512 |
| bin[5] | 148,431 | 12.2% | 520 - 1024 |
| bin[6] | 102,395 | 8.4% | 1032 - 2048 |
| bin[7] | 42,805 | 3.5% | 2056 - 4000+ |

この結果を踏まえて、次のように再分類したが、まだ改善の余地が残ることがわかった。

### 第2回改良後の統計結果

| bin番号 | 要求回数 | 割合 | サイズ範囲 (bytes) |
|---------|----------|------|-------------------|
| bin[0] | 323,831 | 26.7% | 8 - 16 |
| bin[1] | 94,751 | 7.8% | 24 - 32 |
| bin[2] | 56,786 | 4.7% | 40 - 56 |
| bin[3] | 30,776 | 2.5% | 64 - 96 |
| bin[4] | 254,307 | 20.9% | 104 - 160 |
| bin[5] | 100,886 | 8.3% | 168 - 384 |
| bin[6] | 208,463 | 17.2% | 392 - 1024 |
| bin[7] | 145,200 | 12.0% | 1032 - 4000+ |

### 第3回改良後の統計結果

| bin番号 | 要求回数 | 割合 | サイズ範囲 (bytes) |
|---------|----------|------|-------------------|
| bin[0] | 6,263 | 0.5% | 8 |
| bin[1] | 317,568 | 26.1% | 16 |
| bin[2] | 151,537 | 12.5% | 24 - 56 |
| bin[3] | 275,306 | 22.7% | 64 - 128 |
| bin[4] | 19,159 | 1.6% | 136 - 192 |
| bin[5] | 91,504 | 7.5% | 200 - 384 |
| bin[6] | 208,463 | 17.2% | 392 - 1024 |
| bin[7] | 145,200 | 12.0% | 1032 - 4000+ |

ここで、16バイトのメモリ要求が非常に多いということがわかった。

### 第4回改良後の統計結果

| bin番号 | 要求回数 | 割合 | サイズ範囲 (bytes) |
|---------|----------|------|-------------------|
| bin[0] | 323,831 | 26.7% | 8 - 16 |
| bin[1] | 191,750 | 15.8% | 24 - 120 |
| bin[2] | 235,093 | 19.3% | 128 |
| bin[3] | 110,663 | 9.1% | 136 - 384 |
| bin[4] | 208,463 | 17.2% | 392 - 1024 |
| bin[5] | 142,244 | 11.7% | 1025+ |


試行錯誤を繰り返して、16バイトと、128バイトが非常に多いことから、これらをそれぞれbin[0]、bin[1]に振り分けてみたが、なぜか低速になりうまくいかなかった。

結果的に、一番時間がかからなかった、初期のbin分類を採用した。


## 空き領域の左結合を実装

## 空き領域の右結合を実装

