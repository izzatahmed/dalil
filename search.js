/* Browsing families are search aids. Clinical/price equivalence still uses core.alternativeKey. */
import {searchKey,expandSearch} from './core.js?v=0.13.0';
const normalizedQueryCache=new Map(),documentCache=new WeakMap(),ingredientCache=new WeakMap(),phoneticCache=new Map();
const rawQueryKey=value=>expandSearch(value).replace(/\bamoxycillin\b/g,'amoxicillin');
const queryKey=value=>{const key=String(value??'');if(normalizedQueryCache.has(key))return normalizedQueryCache.get(key);const result=rawQueryKey(key);if(normalizedQueryCache.size>300)normalizedQueryCache.clear();normalizedQueryCache.set(key,result);return result;};

export function matchesSearch(group,query,mode='all',contains=false) {
 const tokens=queryKey(query).match(/\d+(?:\.\d+)?|[a-z]+|[\u0621-\u064a]+|%/g)||[];
 const document=prepareDocument(group,mode);
 if(tokens.some(token=>/[\u0621-\u064a]/.test(token))&&!document.phonetic){const labels=mode==='all'?group.record.brand+' '+group.record.scientific:group.record[mode];document.phonetic=new Set((searchKey(labels).match(/[a-z]+/g)||[]).map(phoneticKey).filter(Boolean));}
 return tokens.every(token=>/^\d/.test(token)?document.numbers.has(Number(token)):(/[a-z]/.test(token)?document.words.some(word=>contains&&token.length>=3?word.includes(token):word.startsWith(token)):document.raw.includes(token))||/[\u0621-\u064a]/.test(token)&&arabicTokenMatches(token,document.phonetic));
}

function prepareDocument(group,mode){const source=mode==='all'?group.search:group.record[mode];let cache=documentCache.get(group);if(!cache){cache={};documentCache.set(group,cache);}let document=cache[mode];if(!document||document.source!==source){const raw=(mode==='all'?String(source??''):searchKey(source)).replace(/\bamoxycillin\b/g,'amoxicillin');document=cache[mode]={source,raw,words:raw.match(/[a-z]+|[\u0621-\u064a]+/g)||[],numbers:new Set((raw.match(/\d+(?:\.\d+)?/g)||[]).map(Number))};}return document;}

/* Strip explicit dose/salt notation for browsing only, never for comparisons or source storage. */
export function ingredientNames(record) {
 if(!record?.scientific)return [];
 if(ingredientCache.has(record))return ingredientCache.get(record);
 const source=String(record.scientific).replace(/\([^)]*\)/g,' ');
 const parts=source.split(/[,;+]|\s+&\s+/).map(part=>{
  let name=part.replace(/\b\d+(?:\.\d+)?\s*(?:mg|mcg|ug|µg|g|gm|ml|iu|i\.u\.|units?|%)(?=\b|\s|\/|$)[\s\S]*$/i,'')
   .replace(/\s+as\s+[\s\S]*$/i,'')
   .replace(/\b(?:anhydrous|trihydrate|rrihydrate|monohydrate|dihydrate|hemihydrate|hydrochloride|hcl)\b/ig,'')
   .replace(/\s+/g,' ').trim().replace(/[.\s]+$/,'');
  const key=searchKey(name);
  if(key==='amoxycillin')name='Amoxicillin';
  if(key==='potassium clavulanate')name='Clavulanic Acid';
  return name;
 }).filter(name=>/[a-z\u0621-\u064a]{3}/i.test(name)&&name.length<100&&!/^\d/.test(name));
 const unique=new Map();for(const name of parts)if(!unique.has(searchKey(name)))unique.set(searchKey(name),name);
 const result=[...unique.values()];ingredientCache.set(record,result);return result;
}

export function medicineFamily(record) {
 const names=ingredientNames(record).slice().sort((a,b)=>searchKey(a).localeCompare(searchKey(b),'en'));
 return names.length?names.join(' + '):'';
}

export function matchesFamily(group,family) {
 const wanted=family.split(' + ').map(queryKey).sort(),found=ingredientNames(group.record).map(queryKey).sort();
 if(!wanted.length||!wanted[0]||!found.length)return false;
 // A single-ingredient search includes clearly labelled combinations containing it.
 // An explicitly selected combination keeps the complete ingredient set.
 return wanted.length===1?found.includes(wanted[0]):wanted.length===found.length&&wanted.every((x,i)=>x===found[i]);
}

export function editDistance(a,b,max=2) {
 if(Math.abs(a.length-b.length)>max)return max+1;
 let previous=Array.from({length:b.length+1},(_,i)=>i),beforePrevious;
 for(let i=1;i<=a.length;i++) {
  const current=[i];
  for(let j=1;j<=b.length;j++) {
   current[j]=Math.min(current[j-1]+1,previous[j]+1,previous[j-1]+(a[i-1]===b[j-1]?0:1));
   if(i>1&&j>1&&a[i-1]===b[j-2]&&a[i-2]===b[j-1])current[j]=Math.min(current[j],beforePrevious[j-2]+1);
  }
  beforePrevious=previous;previous=current;
 }
 return previous[b.length];
}

export function makeSearchIndex(groups) {
 const entries=new Map();
 const add=(kind,label,g,family)=>{
  const key=kind+'|'+queryKey(label)+(kind==='brand'?'|'+queryKey(family):'');let x=entries.get(key);
  if(!x){x={kind,label,key:queryKey(label),family,group:g,groups:[],document:{record:{[kind]:label},search:queryKey(label)}};entries.set(key,x);}
  if(!x.groups.includes(g))x.groups.push(g);
 };
 for(const g of groups){
  for(const mode of ['all','brand','scientific'])prepareDocument(g,mode);
  const family=medicineFamily(g.record);add('brand',g.record.brand,g,family);
  const names=ingredientNames(g.record);
  for(const name of names)add('scientific',name,g,name);
  if(names.length>1)add('scientific',family,g,family);
 }
 return [...entries.values()];
}

export function suggestSearch(query,index,mode='all',max=6) {
 const q=queryKey(query);if(q.length<2)return [];
 const eligible=index.filter(x=>mode==='all'||x.kind===mode);
 const entryMatches=(x,value)=>matchesSearch(x.document,value,x.kind)
   ||x.kind==='scientific'&&(queryKey(value).match(/[a-z]+|[\u0621-\u064a]+/g)||[]).some(token=>!['mg','g','ml','mcg','ug','tab','tablet','capsule'].includes(token)&&matchesSearch(x.document,token,x.kind))&&x.groups.some(g=>matchesSearch(g,value,'scientific'));

 const rank=x=>[x.key===q?0:x.key.startsWith(q)?1:2,x.kind==='scientific'?0:1,x.label.split(' + ').length,x.label.length];
 const compare=(a,b)=>{const ar=rank(a),br=rank(b);for(let i=0;i<ar.length;i++)if(ar[i]!==br[i])return ar[i]-br[i];return a.label.localeCompare(b.label,'en',{numeric:true});};
 const result=x=>({label:x.label,query:x.label,kind:x.kind,family:x.family,groupId:x.group.id,count:x.groups.length,spelling:false});
 const direct=eligible.filter(x=>entryMatches(x,q)).sort(compare);
 if(direct.length)return direct.slice(0,max).map(result);
 const match=q.match(/^([a-z]{4,})(.*)$/);if(!match)return [];
 const [,word,rest]=match,seen=new Set(),suggestions=[];
 for(const x of [...eligible].sort(compare)) {
  const candidate=x.key.match(/^[a-z]+/)?.[0];if(!candidate||seen.has(candidate))continue;
  const distance=editDistance(word,candidate,word.length>7?2:1);
  if(!distance||distance>(word.length>7?2:1))continue;
  const corrected=candidate+rest;
  if(!entryMatches(x,corrected))continue;
  seen.add(candidate);suggestions.push({...result(x),label:rest.trim()?corrected:x.label,query:corrected,spelling:true,distance});
 }
 return suggestions.sort((a,b)=>a.distance-b.distance).slice(0,3);
}

export function browseFormRank(form){const f=searchKey(form);if(/^(?:tablet|caplet)$/.test(f)||/^(?:film[- ]coated|coated|chewable|effervescent|dispersible|scored|extended[- ]release|modified[- ]release|prolonged release|release) tablet$/.test(f))return 0;if(/^(?:capsules?|hard capsule|capsule, hard|capsule, soft|soft gelatin capsule)$/.test(f))return 1;if(!/injection|infusion/.test(f)&&/suspension|oral solution|syrup/.test(f))return 2;if(/vial|injection|infusion|ampoule/.test(f))return 8;return 5;}

// Phonetic matching broadens discovery only; original English labels remain visible.
export function phoneticKey(value){const raw=String(value??'');if(phoneticCache.has(raw))return phoneticCache.get(raw);let v=searchKey(raw);if(/[\u0621-\u064a]/.test(v)){v=v.replace(/ه$/,'');const letters={'ا':'a','ب':'b','ت':'t','ث':'t','ج':'j','ح':'h','خ':'kh','د':'d','ذ':'z','ر':'r','ز':'z','س':'s','ش':'sh','ص':'s','ض':'d','ط':'t','ظ':'z','ع':'a','غ':'g','ف':'f','ق':'k','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','و':'w','ي':'y','ء':''};v=[...v].map(c=>letters[c]??c).join('');}const result=v.replace(/ph/g,'f').replace(/sh/g,'x').replace(/ch/g,'k').replace(/th/g,'t').replace(/c(?=[eiy])/g,'s').replace(/[cq]/g,'k').replace(/g/g,'j').replace(/p/g,'b').replace(/v/g,'f').replace(/z/g,'s').replace(/[aeiouwy]/g,'').replace(/[^a-z]/g,'');if(phoneticCache.size>30000)phoneticCache.clear();phoneticCache.set(raw,result);return result;}
function arabicTokenMatches(token,words){const key=phoneticKey(token);if(token.length<3||key.length<2||!words)return false;if(words.has(key))return true;if(token.length<=4)for(const word of words)if(word.startsWith(key))return true;return false;}
export function usesPhoneticSearch(value){return /[\u0621-\u064a]/.test(queryKey(value));}
