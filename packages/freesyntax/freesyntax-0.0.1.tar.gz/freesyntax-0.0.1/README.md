# FreeSyntax
Syntactically Free Python

```py
from freesyntax.factory import RuleFactory
from freesyntax.grammar import Optional, Token, Rule, Match
from freesyntax.structs import AutoLeaf
factory = RuleFactory()

@factory.funcdef(
    Match["def"],
    Token["NAME"],
    Rule["parameters"],
    Optional[Match["->"], Rule["test"]],
    Match["YES"],
    Rule["suite"],
)
def fixer(node):
    node.children[3].replace(AutoLeaf.COLON)


print(factory.transform("""
def a() YES
    pass
"""))

```
