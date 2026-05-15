from pyparsing import (
    alphas,
    alphanums,
    Word,
    Optional,
    Group,
    ZeroOrMore,
    Literal,
    Combine,
    MatchFirst,
    Keyword,
    
)

from constants import (
    k8s_verbs as k8s_v,
    k8s_verbs_name as k8s_vn,
    k8s_verbs_resource_name as k8s_vrn,
    k8s_api_resources,
)

verbs = MatchFirst([Keyword(v).set_name("verb") for v in k8s_v])
verbs_name = MatchFirst([Keyword(v).set_name("verb") for v in k8s_vn])
verbs_resource_name = MatchFirst([Keyword(v).set_name("verb") for v in k8s_vrn])

name = Word(alphas, alphanums + "-_").set_name("name")

resource = MatchFirst([Keyword(r).set_name("resource") for r in k8s_api_resources])

sortFlagKey = Combine(Literal("-") + Word(alphas, exact=1))
longFlagKey = Combine(Literal("--") + Word(alphas, alphanums + "-_"))

flagKey = sortFlagKey | longFlagKey
flagValue = Word(alphas, alphanums + "-_")

flag = Group(flagKey + Optional(flagValue)).set_name("flags")

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

kubectlCommand = Optional("watch") + (verb_resource_name | verb_name | verb).set_name("verb")

typeCommand = resource("resource")

flagCommand = flag("flag")
