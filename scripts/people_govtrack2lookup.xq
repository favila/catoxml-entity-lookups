document{<people>{
let $docpath := '/Users/favila/Documents/workingcopies/deepBills/deepbills/people.xml'
, $doc := doc($docpath)
return ($doc/people/@session, 
  for $p in $doc/people/person
  return <person
    id="{$p/@bioguideid}"
    govtrackid="{$p/@id}"
  >{($p/@title, $p/@state, $p/@class, $p/@district, $p/@party)}
    <name>{$p/@lastname, $p/@firstname, translate($p/@name, '[]', '()')}</name>
  </person>
)}</people>}