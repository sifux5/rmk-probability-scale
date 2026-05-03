"""
Bayesian reasoning about Estonian forest fire risk by tree species.

We estimate the probability that a forest fire occurs in a conifer stand
using Bayes' theorem, given that conifers are known to burn more readily
than deciduous trees.

Prior knowledge:
  - P(conifer) = share of conifer forest in Estonia (from KK51.PX)
  - Likelihood ratio: conifers burn ~3x more often than deciduous forest
    (Causley et al. 2016, European forest fire statistics)

Bayes' theorem:
  P(conifer | fire) = P(fire | conifer) * P(conifer) / P(fire)
"""


def bayes_fire_given_conifer(p_conifer: float, likelihood_ratio: float = 3.0) -> dict:
    """
    Estimate P(fire | conifer) and P(conifer | fire) using Bayes' theorem.

    Args:
        p_conifer: Prior probability that a random forest hectare is conifer.
        likelihood_ratio: How many times more likely a fire is in conifer vs
                          deciduous forest. Default 3.0 based on European data.

    Returns:
        Dict with prior, likelihood, posterior, and interpretation.
    """
    p_deciduous = 1 - p_conifer

    # Normalise so that weighted average = 1 (relative likelihoods)
    # P(fire | conifer)   = likelihood_ratio * k
    # P(fire | deciduous) = 1 * k
    # P(fire) = P(fire|conifer)*P(conifer) + P(fire|deciduous)*P(deciduous) = 1*k
    k = 1 / (likelihood_ratio * p_conifer + p_deciduous)

    p_fire_given_conifer = likelihood_ratio * k
    p_fire_given_deciduous = k
    p_fire = p_fire_given_conifer * p_conifer + p_fire_given_deciduous * p_deciduous

    # Bayes: P(conifer | fire)
    p_conifer_given_fire = (p_fire_given_conifer * p_conifer) / p_fire

    return {
        "p_conifer_prior": round(p_conifer, 4),
        "p_conifer_given_fire": round(p_conifer_given_fire, 4),
        "p_fire_given_conifer_relative": round(p_fire_given_conifer, 4),
        "likelihood_ratio": likelihood_ratio,
    }


if __name__ == "__main__":
    result = bayes_fire_given_conifer(p_conifer=0.4292)

    print("Bayesi analüüs: tulekahjurisk okaspuumetsas")
    print(f"  Okaspuu osakaal metsast (prior):       {result['p_conifer_prior']:.1%}")
    print(f"  Okaspuu osakaal tulekahjudest (post):  {result['p_conifer_given_fire']:.1%}")
    print(f"  Tulekahjude suhteline risk okaspuus:   {result['likelihood_ratio']}x suurem")
    print()
    print("Tõlgendus: kuigi okaspuud moodustavad 43% metsast,")
    print(f"toimub {result['p_conifer_given_fire']:.0%} tulekahjudest okaspuumetsas.")