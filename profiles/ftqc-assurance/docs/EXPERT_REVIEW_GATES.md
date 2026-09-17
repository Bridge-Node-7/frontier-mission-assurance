# Expert Review Gates

FTQC Assurance stops where qualified domain judgment is required.

An expert adjudication records the exact question, competency domain, evidence reviewed, conclusion, known exclusions, unresolved uncertainty, and conditions that reopen the review.

## Review classes

- `INTERNAL_DOMAIN_REVIEW` — qualified review inside the program or organization responsible for the work.
- `EXTERNAL_DOMAIN_REVIEW` — qualified outside review that is not represented as independent V&V.
- `INDEPENDENT_VV_REVIEW` — review explicitly governed as independent verification or validation under the applicable process.

These classes are not interchangeable.

## Conclusions

The public contract allows:

- `SUPPORTED_WITHIN_SCOPE`
- `REVIEW_REQUIRED`
- `NOT_REVIEWED`
- `NOT_SUPPORTED_WITHIN_SCOPE`

A mandatory review that is not `SUPPORTED_WITHIN_SCOPE` prevents an `APPROVE` decision in the synthetic reference policy.

## Reopen conditions

Expert judgment is versioned context, not timeless authority. A review can name assumption or evidence references that force reconsideration when they change.
