ال `dpi` بتاع الfigure بيتضاعف كل مره اعمل unpickle للfigure علي MacOSX backend علي ماك M1 الrepro [[A1]] بيعمل pickle/unpickle لنفس الfigure 32 مره في loop ويطبع `fig.dpi`
اللي بيحصل [[A2]] الdpi بيروح 200 -> 400 -> 800 ... وبعدين بيضرب `OverflowError: signed integer is greater than maximum` من `FigureCanvas.__init__` في `backend_macosx` جاي من `Figure.__setstate__`
المتوقع [[A3]] الdpi يفضل `200.0` بعد كل round trip
matplotlib 3.5.2 و macOS 12.4 arm64 وبيحصل علي ماك بوك M1 بس ونسخه البايثون مش فارقه خالص
