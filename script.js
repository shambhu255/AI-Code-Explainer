const codeEl=document.getElementById("code"), output=document.getElementById("output"), errorBox=document.getElementById("error"), copyBtn=document.getElementById("copy");
codeEl.addEventListener("input",()=>document.getElementById("charCount").textContent=codeEl.value.length.toLocaleString()+" characters");
document.getElementById("clear").addEventListener("click",()=>{codeEl.value="";codeEl.dispatchEvent(new Event("input"));output.className="output";output.innerHTML='<div class="empty-icon">✦</div><h3>Your result will appear here</h3><p>Choose an action above to analyse your code.</p>';errorBox.hidden=true;copyBtn.disabled=true;});
document.getElementById("file").addEventListener("change",async e=>{const f=e.target.files[0];if(!f)return;if(f.size>2*1024*1024){showError("File is larger than 2 MB.");return;}codeEl.value=await f.text();codeEl.dispatchEvent(new Event("input"));});
function showError(msg){errorBox.textContent=msg;errorBox.hidden=false;}
document.querySelectorAll("[data-task]").forEach(btn=>btn.addEventListener("click",async()=>{
 const code=codeEl.value.trim();errorBox.hidden=true;
 if(!code){showError("Paste or upload source code first.");codeEl.focus();return;}
 document.querySelectorAll("[data-task]").forEach(b=>b.disabled=true);
 output.className="output";output.textContent="Analysing your code…";output.classList.add("loading");copyBtn.disabled=true;
 try{
  const res=await fetch("/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({code,task:btn.dataset.task,language:document.getElementById("language").value})});
  const data=await res.json();if(!res.ok)throw new Error(data.error||"Something went wrong.");
  output.classList.remove("loading");output.classList.add("has-result");output.textContent=data.result;copyBtn.disabled=false;
 }catch(err){output.classList.remove("loading");output.textContent="No result generated.";showError(err.message);}
 finally{document.querySelectorAll("[data-task]").forEach(b=>b.disabled=false);}
}));
copyBtn.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(output.textContent);copyBtn.textContent="Copied!";setTimeout(()=>copyBtn.textContent="Copy result",1300);}catch{showError("Clipboard access was blocked by your browser.");}});
