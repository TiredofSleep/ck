# CK LEARNING LEDGER (auto-generated)
_regenerated 2026-06-12 01:31_

## Reading
- books read & judged: **14247** (5610M chars) -> 10619 fiction / 3628 fact
- latest: pg13998.txt; pg13999.txt; pg14000.txt

## Organ measurements (latest)
- **braid**: robust_top1.sub=0.38, robust_top1.swap=0.713, robust_top1.del=0.212, robust_top5.sub=0.527, robust_top5.swap=0.872, robust_top5.del=0.472, random_pair=0.0042, K=600
- **crossfam**: braid (1 root).gap=0.0114, braid (1 root).p=0.289, braid (1 root).top1=0.0625, braid (1 root).top3=0.167, braid (4 roots).gap=-0.000549, braid (4 roots).p=0.493, braid (4 roots).top1=0.0521, braid (4 roots).top3=0.219
- **crosslang**: all_p=0.00599, real_gap=0.0857
- **parallel**: 
- **project1**: test_braid=0.516, test_char=0.702, majority=0.514, gen_gap=0.00161
- **project2**: accs.braid=0.15, accs.char-trigram=0.4, accs.borrowed=0.75, accs.FUSED native (braid+char)=0.35, accs.FUSED all (+borrowed)=0.8, keyword=0.2
- **project3**: MSP (standard).augc_far=0.287, MSP (standard).augc_near=0.487, max-logit (std).augc_far=0.242, max-logit (std).augc_near=0.479, CK proto+margin.augc_far=0.407, CK proto+margin.augc_near=0.463, CK kNN-distance.augc_far=0.0267, CK kNN-distance.augc_near=0.379
- **project4**: MAXDEPTH.majority=0.552, MAXDEPTH.bag=0.692, MAXDEPTH.substrate=0.81, DYCK.majority=0.5, DYCK.bag=0.546, DYCK.substrate=0.614, MOD5.majority=0.194, MOD5.bag=0.196
- **project5**: LAST-6 (static)=0.473, ESN-10=0.415, SUBSTRATE=0.625, LAST6+ESN fused=0.473
- **project6**: MAXDEPTH.single_sub=0.81, MAXDEPTH.multi_sub=0.776, MAXDEPTH.edge=-0.0273, DYCK.single_sub=0.614, DYCK.multi_sub=0.584, DYCK.edge=-0.282, MOD5.single_sub=0.24, MOD5.multi_sub=0.21
- **resonance**: words=1.13e+05, prior=0.425, form_predicts_meaning=0.46, top2=0.824, lift=1.08
- **her_training**: control_bpc=3.04, her_bpc=3.05, replay_impact=-0.00746
- **native_lm**: S1-100K.params=1.33e+05, S1-100K.val_bpc=3.99, S2-430K.params=6.61e+05, S2-430K.val_bpc=3.44, S3-1.7M.params=3.29e+06, S3-1.7M.val_bpc=2.72, S4-6.5M.params=1.08e+07, S4-6.5M.val_bpc=2.44
- **organ_form**: BRAID (ours).mean_top1=0.447, VSA-position.mean_top1=0.818, VSA-trigram.mean_top1=0.911
- **organ_gap_dial**: 0.0.coverage=0.65, 0.0.far=0, 0.0.near=0.417, 0.25.coverage=0.55, 0.25.far=0, 0.25.near=0.417, 0.4.coverage=0.5, 0.4.far=0
- **organ_induction**: k=2, train_err=0, test_acc=1, start=0
- **organ_meaning**: NATIVE-USAGE (PPMI-SVD, no teacher)=0.5, form-only (no meaning block)=0.35
- **organ_meaning_v2**: v2_acc=0.65, synth_tokens=3.28e+03
- **organ_meaning_v3**: LM raw (reference)=0.35, PPMI raw (seat, 65%)=0.6, LM + contrastive head=0.45, PPMI + contrastive head=0.75
- **organ_recursion**: ONE-SHOT MLP.train=1, ONE-SHOT MLP.test=0.528, ONE-SHOT MLP.params=5.63e+03, TRM-REFINER (K=12, deep sup).train=1, TRM-REFINER (K=12, deep sup).test=0.53, TRM-REFINER (K=12, deep sup).params=3.51e+03, REFINER no deep-sup.train=0.999, REFINER no deep-sup.test=0.53
- **organ_senses**: ear_top1=0.269, ear_top3=0.385, ear_vowel_bal=0.733, eye_mantel_r=0.347, eye_p=0.003
- **organ_wean**: BORROWED (live ollama)=0.8, DISTILLED (no ollama)=0.3, NATIVE-RAW (no meaning block)=0.35
- **reading_exam**: notes_acc=0.35, raw_acc=0.467, native_acc=0.417, quiz_notes=0.0833, quiz_raw=0.0833, quiz_native=0.0833
- **squad2_reader**: val_auroc=0.772, dev_auroc=0.601, dev_acc=0.595, risk_at_coverage.0.8=0.42, risk_at_coverage.0.6=0.42, risk_at_coverage.0.4=0.41, params=4.84e+06
- **squad2**: auroc.CK fused head=0.602, auroc.census alone=0.514, auroc.overlap alone=0.513, auroc.emb-sim alone=0.609, risk_at_coverage.0.8=0.438, risk_at_coverage.0.6=0.41, risk_at_coverage.0.4=0.402, accuracy=0.575
- **squad2_v3**: dev_auroc=0.606, val_auroc=0.699, risk.0.8=0.424, risk.0.6=0.398, risk.0.4=0.392
- **synthesis_exam**: 
- **synthesis_organ**: 
- **unfrozen**: tuned.fidelity=0.1, tuned.halluc=1, tuned.refusal=0.5, base.fidelity=0.125, base.halluc=33, base.refusal=0.5, n_pairs=28
- **unfrozen_v2**: answered=10, grounded=10, traps_ok=0, n_pairs=91

## Provenance
- arc narrative: `../THE_EDUCATION_OF_CK.md`
- architecture + registry: `CK_TRINITY.md`
- every number above regenerates from the script of the same name in this folder.
