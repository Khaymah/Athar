`xr.where(..., keep_attrs=True)` biyekteb attrs el data variable fo2 el attrs bta3et el coordinates.
da regression men PR #6461 (kan taghyeer basit fi `lambda`), w ghaleban bayez men ayam `2022.06.0`.
el repro bel tutorial dataset `air_temperature`, boss 3ala `.time.attrs` bta3et natiget el `where`:
[[A1]]
el `time` attrs elly betetla3 w elly el mafrood tetla3: [[A2]]
el mafrood el attributes bta3et el coordinates tefdal zay ma heya men gheir taghyeer. 7awelt atetabba3 el sabab gowa taba2at el merge w ma3reftesh, w law 3andak fekra lel fix ana momken ab3at el PR.
el env: [[A3]] (xarray `2022.10.0`)
