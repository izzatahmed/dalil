/* Suggestions are navigation aids. They never change source records or substitute a medicine. */
import {searchKey,expandSearch} from './core.js?v=0.6.0';

export function matchesSearch(group, query, mode='all') {
  const tokens=expandSearch(query).match(/\d+(?:\.\d+)?|[a-z]+|[\u0621-\u064a]+|%/g)||[];
  const raw=mode==='all'?group.search:searchKey(group.record[mode]);
  const words=(raw.match(/\d+(?:\.\d+)?|[a-z]+|[\u0621-\u064a]+|%/g)||[]);
  return tokens.every(token=>/^\d/.test(token)?words.some(w=>/^\d/.test(w)&&Number(w)===Number(token)):raw.includes(token));
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
  const seen=new Set(),entries=[];
  for(const g of groups)for(const kind of ['brand','scientific']) {
    const label=g.record[kind];if(!label)continue;
    const key=kind+'|'+searchKey(label);if(seen.has(key))continue;seen.add(key);
    entries.push({kind,label,key:searchKey(label),group:g});
  }
  return entries;
}

export function suggestSearch(query,index,mode='all',max=6) {
  const q=expandSearch(query);if(q.length<2)return [];
  const eligible=index.filter(x=>mode==='all'||x.kind===mode);
  const direct=eligible.filter(x=>matchesSearch({record:{[x.kind]:x.label},search:x.key},q,x.kind))
    .sort((a,b)=>(a.key===q?0:a.key.startsWith(q)?1:2)-(b.key===q?0:b.key.startsWith(q)?1:2)||a.label.localeCompare(b.label,'en',{numeric:true}));
  if(direct.length)return direct.slice(0,max).map(x=>({label:x.label,query:x.label,kind:x.kind,spelling:false}));
  const match=q.match(/^([a-z]{4,})(.*)$/);if(!match)return [];
  const [,word,rest]=match,seen=new Set(),suggestions=[];
  for(const x of eligible) {
    const candidate=x.key.match(/^[a-z]+/)?.[0];if(!candidate||seen.has(candidate))continue;
    const distance=editDistance(word,candidate,word.length>7?2:1);
    if(!distance||distance>(word.length>7?2:1))continue;
    const corrected=candidate+rest;
    // Every remaining numeric/formulation token must still match the proposed record.
    if(!matchesSearch(x.group,corrected,x.kind))continue;
    seen.add(candidate);suggestions.push({label:corrected,query:corrected,kind:x.kind,spelling:true,distance});
  }
  return suggestions.sort((a,b)=>a.distance-b.distance||a.label.localeCompare(b.label)).slice(0,3);
}
