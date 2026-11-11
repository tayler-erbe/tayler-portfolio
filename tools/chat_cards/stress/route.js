// node route.js questions.json out.json  -> for each question: what the chat shows (hybrid search, as in the browser)
const fs=require("fs"),path=require("path");const root="/home/user/tayler-portfolio";
global.window={matchMedia:()=>({matches:false}),innerWidth:1000,addEventListener(){}};
global.document={readyState:"loading",addEventListener(){},documentElement:{},querySelector(){return null},currentScript:{src:"x/chat.js"},getElementsByTagName(){return[]},createElement(){return{setAttribute(){},appendChild(){},addEventListener(){},style:{}}},head:{appendChild(){}},body:{appendChild(){}}};
eval(fs.readFileSync(root+"/assets/chat/chat.js","utf8"));
(async()=>{
const kb=JSON.parse(fs.readFileSync(process.env.KB||root+"/assets/chat/kb.json","utf8"));const eng=new window.AskTayler.Engine(kb);
const buf=fs.readFileSync(process.env.EMB||root+"/assets/chat/kb_emb.bin");const head=eng.setEmbeddings(buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.length));
const lib=await import("/home/user/jobhunter/chatbot/emb/node_modules/@huggingface/transformers/dist/transformers.mjs");lib.env.allowLocalModels=false;
const fe=await lib.pipeline("feature-extraction",head.model,{revision:head.revision,dtype:head.dtype||"q8"});
const qs=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));const out=[];
for(let i=0;i<qs.length;i+=64){const b=qs.slice(i,i+64);const r=await fe(b.map(x=>x.q.slice(0,200)),{pooling:"mean",normalize:true});const d=r.dims[1];
 b.forEach((x,j)=>{const v=new Float32Array(r.data.slice(j*d,(j+1)*d));const q=x.q.slice(0,200);const h=eng.search(q,v),bm=eng.search(q);
  const c=h.confident&&h.best?h.best.card:null;
  out.push({...x,id:c?c.id:null,title:c?c.title:null,answer:c?c.answer||(c.state==="PENDING"?"(pending card: 'not answered yet')":""):null,
   related:(h.related||[]).map(r=>r.card.id),bm25:bm.confident&&bm.best?bm.best.card.id:null,runner:(h.ranked||bm.all||[]).slice(0,4).map(r=>r.card.id)});});}
fs.writeFileSync(process.argv[3],JSON.stringify(out,null,1));
console.log("routed",out.length,"answered",out.filter(o=>o.id).length,"declined",out.filter(o=>!o.id).length);
})();
