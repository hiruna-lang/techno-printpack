'use strict';
const contactForm=document.querySelector('#contact-form');
const contactStatus=document.querySelector('#contact-status');
const contactPreview=document.querySelector('#contact-preview');
const contactConfig=window.TECHNO_CONFIG||{whatsappNumber:'',enquiryEmail:'info@technoind.biz'};
const contactWhatsApp=document.querySelector('#contact-whatsapp');
let contactMessage='';
contactWhatsApp.disabled=!/^\d{8,15}$/.test(contactConfig.whatsappNumber);
if(!contactWhatsApp.disabled)document.querySelector('#contact-whatsapp-note').textContent='Review and send your enquiry directly in WhatsApp.';
function validateContact(field){
 let error='';
 if(!field.value.trim())error='Please complete this field.';
 else if(field.type==='email'&&!field.validity.valid)error='Enter a valid email address.';
 else if(field.name==='phone'&&(!/^[+()\d\s.-]{7,24}$/.test(field.value)||field.value.replace(/\D/g,'').length<7))error='Enter a valid contact number.';
 field.setAttribute('aria-invalid',String(Boolean(error)));
 document.querySelector(`#contact-${field.name}-error`).textContent=error;
 return !error;
}
contactForm.querySelectorAll('[required]').forEach(field=>field.addEventListener('blur',()=>validateContact(field)));
function prepareContact(){
 const fields=[...contactForm.querySelectorAll('[required]')];
 const validity=fields.map(validateContact);
 if(validity.includes(false)){fields[validity.indexOf(false)].focus();contactStatus.textContent='Please check the highlighted fields.';return false;}
 const data=new FormData(contactForm);
 contactMessage='Techno Printpack — '+data.get('subject')+'\n\n'+[['name','Name'],['company','Company / Organization'],['email','Email'],['phone','Contact Number'],['message','Message']].map(([key,label])=>`${label}: ${String(data.get(key)||'Not specified').trim()}`).join('\n');
 document.querySelector('#contact-message-preview').textContent=contactMessage;
 document.querySelector('#contact-email-draft').href=`mailto:${contactConfig.enquiryEmail}?subject=${encodeURIComponent(data.get('subject'))}&body=${encodeURIComponent(contactMessage)}`;
 contactPreview.hidden=false;contactStatus.textContent='Message prepared for review. Nothing has been sent.';
 return true;
}
contactForm.addEventListener('submit',e=>{e.preventDefault();if(prepareContact())contactPreview.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'nearest'});});
contactForm.addEventListener('input',()=>{if(!contactPreview.hidden){contactPreview.hidden=true;contactStatus.textContent='Details changed. Prepare your message again to update it.';}});
contactWhatsApp.addEventListener('click',()=>{if(!contactWhatsApp.disabled&&prepareContact())window.open(`https://wa.me/${contactConfig.whatsappNumber}?text=${encodeURIComponent(contactMessage)}`,'_blank','noopener,noreferrer');});
document.querySelector('#contact-copy').addEventListener('click',async()=>{
 try{await navigator.clipboard.writeText(contactMessage);contactStatus.textContent='Message copied. Paste it into your email or messaging app and send when ready.';}
 catch{const range=document.createRange();range.selectNodeContents(document.querySelector('#contact-message-preview'));getSelection().removeAllRanges();getSelection().addRange(range);contactStatus.textContent='Use your device’s copy command to copy the highlighted message.';}
});
