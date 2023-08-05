# ServoMotor
RCサーボモーターはコンピューターの入っているギヤードモーターです。
角度を維持することができます。
ただ角度をモーターに指示するだけで良いのです。

![](./servomotor.gif)

### 電源もobnizに繋げられるモーターについて

RCサーボの多くは電源も含めそのままobnizに接続できますが、いくつかの(特に小型の）サーボモーターでは電源の電流がリークしやすくobnizの過電流検知により電源を供給できない場合があります。

その場合は以下のような対策が必要となります。

- （推奨）電源のみ外部から供給する(obnizのJ1ピンはUSB直結なのでそこから供給することもできます)
- ブレッドボードを介してobnizと接続する(ブレッドボードは抵抗が大きく、過電流検知を回避できることがあります。)

obnizのioから直接電源供給を確認したサーボモーター

メーカー | 型番
--- | ---
Tower Pro | SG-5010
Tower Pro | MG92B
Tower Pro | MG90S
Tower Pro | MG90D
Tower Pro | SG90
Tower Pro | SG92R
GWS | S35STD

obnizのioからでは直接電源供給できないサーボモーター

メーカー | 型番
--- | ---
Quimat | QKY66-5
FEETECH | FS90R

## obniz.wired("ServoMotor", {[vcc, gnd, signal, pwm]})
３本の足をObnizにつなぎます。それぞれプラス、信号、マイナスとなっていて、製造メーカーなどにより配置が違います。

この例はもっともよく使われている配線パターンです。
obnizのセットに入っているサーボモーターもこのパターンです。

![](./servocable.jpg)

信号(signal)、プラス(vcc)、マイナス(gnd)をそれぞれ obnizの0, 1, 2につないだ場合は以下のようにします。

![](./wired.png)
```Python
# Python Example
servo = obniz.wired("ServoMotor", {"signal": 0, "vcc": 1, "gnd": 2})
servo.angle(90.0) # half position
```

vccとgndを他の方法で接続している場合はsignalのみの指定でOKです
```Python
servo = obniz.wired("ServoMotor", {"signal": 2})
```

また、生成済みのpwmオブジェクトを利用することも出来ます
```Python
pwm = obniz.get_free_pwm()
servo = obniz.wired("ServoMotor", {"pwm": pwm})
```

## angle(degree)
角度を0~180により指定します。

```Python
# Python Example
servo = obniz.wired("ServoMotor", {"signal": 0, "vcc": 1, "gnd": 2})

servo.angle(90.0) # half position
```

## range = {min, max}

出力するパルス幅を調整できます。
0度~180度に応じて0.5~2.4msecのパルスが出力されますが、それを自分で調整したい場合に利用します。

```Python
# Python Example
servo = obniz.wired("ServoMotor", {"signal": 0, "vcc": 1, "gnd": 2})
servo.range = {
  "min": 0.8,
  "max": 2.4
}
servo.angle(90.0) # half position
```

## on()
サーボモーターの電源を入れます。wiredを呼んだ段階で電源は入っています。offにした後に再度onにしたい時に呼んでください

```Python
# Python Example
servo = obniz.wired("ServoMotor", {"signal": 0, "vcc": 1, "gnd": 2})

servo.angle(90.0) # half position
servo.off()
servo.on()
```
## off()
サーボモーターの電源を切ります。信号の供給も停止します。保持力がなくなりますから、モーターに負荷がかかっている場合はoffにすることで勝手に回転します。

```Python
# Python Example
servo = obniz.wired("ServoMotor", {"signal": 0, "vcc": 1, "gnd": 2})

servo.angle(90.0) # half position
servo.off()
servo.on()
```