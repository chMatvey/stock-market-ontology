import pylode

html = pylode.MakeDocco(
    input_data_file='../../Stock-market-ontology.owl',
    outputformat="html",
    profile="ontdoc"
).document()

f = open("../../documentation.html", "a")
f.write(html)
f.close()