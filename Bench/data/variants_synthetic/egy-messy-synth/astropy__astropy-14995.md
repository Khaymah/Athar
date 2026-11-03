فى astropy `5.3` الmask propagation فى الarithmetic بتاع `NDDataRef` بتضرب لما واحد من الاتنين ملوش mask وده كان shaghal 3ady فى `5.2`
بيحصل مع `handle_mask=np.bitwise_or` بيطلع `TypeError` على `|` بين `int` و `NoneType`
اهو السيشن [[A1]] mask فى constant و mask فى حاجه ملهاش mask بيضربو انما من غير mask خالص او mask فى mask شغالين
الفيرجنز [[A2]]
تخمينى ان الماسك الى مش موجود بيتعامل كانه `None`s فا `bitwise_or` بتاخد int و `None`
المفروض لو واحد بس ليه mask يتنسخ هو نفسه فى الاوتبوت زى ما كان بيحصل في v5.2
