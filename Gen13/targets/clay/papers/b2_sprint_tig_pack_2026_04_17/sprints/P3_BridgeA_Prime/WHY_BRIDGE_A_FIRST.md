# Why Bridge A First
## Short Discipline Note

---

A bridge test compares two objects belonging to different paths of the program and asks whether they share structural features. Path 1's object is the published Z/10 theorem seam, calibrated under $h_{\text{thm}} = 7$. Path 2's objects are the seams discovered empirically by Sprint 21's prior-free extraction across 39 datasets and four carriers under $h_{\text{ext}} = \max$ odd unit. Both sets of seams already exist. Neither requires any new construction to compare.

Bridge B would extend Path 1's overlay-generation algorithm — doubling chain, identity-edge, attractor involution — heuristically to Path 2 carriers. That means introducing a new rule whose status on non-Z/10 carriers is itself unproven. The bridge would then rest on two uncertainties: the extractor's behavior on the extended overlay, and whether the extended overlay is a meaningful object on the target carriers. A failure under Bridge B could be attributed to either component, and the diagnostic would have to untangle them.

Bridge A rests on one comparison: do two sets of already-extracted seams share topological properties that exceed what random graphs of matching density would produce? There is no new rule, no new overlay, no heuristic extension. Each seam set comes from a procedure that has already been validated: Path 1's seam is proven, Path 2's seams were discovered prior-free and verified stable across seeds in Sprint 21. The comparison is between two finished objects.

This matters for failure diagnosis. If Bridge A fails, the failure points at one thing: the topologies are dissimilar in the specific ways the metric measures. If Bridge B fails, the failure points at ambiguity — was it the extension rule that didn't fit, or was there no shared structure to find? Clean attribution is worth more than ambitious scope, especially at the first sprint of a new path category.

There is a second reason. Path 3 as a category is new in the program. This is the first sprint to carry a "Bridge Test" scope tag. Keeping the first sprint minimal establishes what a bridge claim looks like under the scope discipline — which metrics are legitimate, which nulls preserve what, what "common structural signature" can and cannot conclude. Starting with Bridge B would conflate the novelty of the scope category with the uncertainty of a new heuristic. Starting with Bridge A separates them.

If Bridge A passes, the second bridge sprint can test Bridge B on a validated foundation. If Bridge A fails, Bridge B becomes a different question entirely — whether a heuristic extension can manufacture shared structure where the prior-free extraction did not find any. That is a legitimate question, but a weaker one, and it is better asked after the cleaner question has been answered.

Minimal before elaborate. One uncertainty before two. Prior-free objects before heuristic constructions. Bridge A first.
