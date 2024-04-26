from pyparsing import (
    Word,
    alphas,
    Optional,
    Group,
    ZeroOrMore,
    Literal,
    Combine,
    alphanums,
    MatchFirst,
    Keyword,
)

from constants import (
    k8s_verbs,
    k8s_verbs_name,
    k8s_verbs_resource_name,
    k8s_api_resources,
)

verbs = MatchFirst([Keyword(v).setName("verb") for v in k8s_verbs])
verbs_name = MatchFirst([Keyword(v).setName("verb") for v in k8s_verbs_name])
verbs_resource_name = MatchFirst(
    [Keyword(v).setName("verb") for v in k8s_verbs_resource_name]
)
name = Word(alphas, alphanums + "-_").setName("name")

resource = MatchFirst([Keyword(r).setName("resource") for r in k8s_api_resources])

sortFlagKey = Combine(Literal("-") + Word(alphas, exact=1))
longFlagKey = Combine(Literal("--") + Word(alphas, alphanums + "-_"))

flagKey = sortFlagKey | longFlagKey
flagValue = Word(alphas, alphanums + "-_")

flag = Group(flagKey + Optional(flagValue)).setName("flags")

verb_resource_name = (
    verbs_resource_name("resource")
    + ZeroOrMore(flag("resource"))
    + resource("name flags")
    + Optional(name("flags"))
    + ZeroOrMore(flag("flags"))
)

verb_name = (
    verbs_name("name")
    + ZeroOrMore(flag)("name")
    + name("flags")
    + ZeroOrMore(flag("flag"))
)

verb = verbs("flags") + ZeroOrMore(flag("flags"))

kubectlCommand = (verb_resource_name | verb_name | verb).setName("verb")

typeCommand = resource("resource")

flagCommand = flag("flag")
