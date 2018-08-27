import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(u"gave ten large apples to her mother")

chunks=[]
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text)
    chunks.append(chunk.root.dep_)

print chunks
