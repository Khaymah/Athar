عندي مشكل ف `NDDataRef`: la propagation ديال الmask ف les opérations arithmétiques كتطيح ف astropy `5.3` ملي واحد من les opérandes ماعندوش mask، وف `5.2` كانت خدامة مزيان.
كيوقع هادشي مع `handle_mask=np.bitwise_or`، كيطلع ليا `TypeError` على `|` بين `int` و `NoneType`.
هاهي la session باش تعاودها، mask × constante و mask × بلا mask كيطيحو، أما الحالات بلا mask و mask × mask خدامين:
[[A1]]
كنظن بلي الmask اللي ماكاينش كيتعامل معاه بحال شي `None`s، داكشي علاش `bitwise_or` كتجيها int و `None`.
اللي بغيت: إلا كان غير واحد فيهم عندو mask، خاصو يتكوبيا داك الmask ف le résultat بحال ما كان ف v5.2.
les versions: [[A2]]
