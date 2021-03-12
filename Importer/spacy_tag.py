import spacy
from spacy import displacy

nlp_wk = spacy.load('en_core_web_sm')
# nlp_wk = spacy.load('xx_ent_wiki_sm')
doc = nlp_wk(" WonderLa Amusement park Multiple tornado warnings were amusement park water park issued for parts of New York on Sunday night.The first warning, which expired at 9 p.m., covered the Bronx, Yonkers and New Rochelle. More than 2 million people live in the impacted area.")

res = displacy.render(doc, style="ent")

print(res)