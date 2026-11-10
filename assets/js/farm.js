'use strict';
document.querySelector('#year').textContent=new Date().getFullYear();
const form=document.querySelector('#enquiry-form');
function selectProduce(value){if([...form.elements.produce.options].some(o=>o.value===value))form.elements.produce.value=value}
selectProduce(new URLSearchParams(location.search).get('produce'));
document.querySelectorAll('[data-produce]').forEach(a=>a.addEventListener('click',()=>selectProduce(a.dataset.produce)));
form.addEventListener('submit',e=>{e.preventDefault();const data=new FormData(form);const subject='Green Techno Farm enquiry: '+form.elements.produce.selectedOptions[0].text;const body=`Name: ${data.get('name')}\nEmail: ${data.get('email')}\nPhone: ${data.get('phone')}\nProduce: ${form.elements.produce.selectedOptions[0].text}\n\n${data.get('message')}`;location.href='mailto:info@technoind.biz?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);document.querySelector('#form-status').textContent='Your enquiry is ready in your email app. Please send it there, or contact info@technoind.biz directly.'});
const dialog=document.querySelector('.lightbox');
document.querySelectorAll('.gallery-photo').forEach(button=>button.addEventListener('click',()=>{const source=button.querySelector('img');dialog.querySelector('img').src=source.src;dialog.querySelector('img').alt=source.alt;dialog.querySelector('p').textContent=source.alt;dialog.showModal()}));
dialog.querySelector('button').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
