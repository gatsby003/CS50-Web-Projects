
// documenatation done! project done!!

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#archive-btn").addEventListener('click', () => archive_or_unarchive(content));
  document.querySelector('#reply-btn').addEventListener('click', () => reply_to_email(content.sender, content.subject));

  // listen for submission of email
  document.querySelector("#compose-form").onsubmit = () => {
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
    console.log(recipients, body, subject);
    if (recipients.length === 0 || subject.length === 0 || body.length === 0){
      alert("No one likes incomplete emails!")
    }
    else {
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result)
      });
    }

    load_mailbox('sent');

    return false
  }
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#show-mails-view').style.display = 'none';
  document.querySelector('#email-options-view').style.display = 'none';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#show-mails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-options-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // make api request 
  console.log('this is a good life')
  fetch(`/emails/${mailbox}`,{
    method : 'GET',
    }).
    then(response => response.json()).
    then(result => {
      for (let i = 0; i < result.length; i = i + 1){
        add_mail(result[i], mailbox);
      }
    })
   
}

// helper function for loading function in mail-boxes
add_mail = (content, mailbox) => {
  const mail = document.createElement('div');
  mail.setAttribute('id', 'post-id')
  mail.addEventListener('click', () => showMail(content, mailbox))
  if (content.read){
    mail.className = 'post read'
  }
  else{
    mail.className = 'post unread'
  }
  if (mailbox === 'sent'){
    console.log("innnn")
    mail.innerHTML += `<p>To : ${content.recipients[0]}...</p>`
  }
  else {
    mail.innerHTML += `<p>From : ${content.sender}</p>`
  }

  mail.innerHTML += `<a><p>Time : ${content.timestamp}Subject: ${content.subject}</a></p>`
  document.querySelector('#emails-view').append(mail);
}

// loading singular mail view 
showMail = (content, mailbox) => {
  // bigass function that manages the entire individual-email view 

  // clear view
  document.querySelector('#show-mails-view').innerHTML = ''

  // mark email as read
  mark_as_read(content)

  // figure out which button to show based on mailbox
  document.querySelector('#email-options-view').style.display = 'block';
  if (mailbox == 'sent'){
    document.querySelector("#archive-btn").style.display = 'none';
  }

  // marking button as archive or unarchive based on mailbox type
  archive_btn = document.querySelector('#archive-btn');
  if (mailbox === "archive"){
    archive_btn.innerHTML = "Unarchive"
  }
  else {
    archive_btn.innerHTML = "Archive"
  }

  // child elements to hold content 
  const header = document.createElement('div');
  const mailbody = document.createElement('div');

  // set header 
  if (mailbox === sent){ header.innerHTML += `<p>Recipients : ${content.recipients[0]}...<hr>`}
  else { header.innerHTML += `<p>Sender : ${content.recipients[0]}<hr>`}
  header.innerHTML += `Time : ${content.timestamp}</p>`
  document.querySelector('#show-mails-view').append(header)

  // set body
  mailbody.innerHTML += `<p>${content.body}</p>`
  document.querySelector('#show-mails-view').append(mailbody)

  // append mail to dom
  document.querySelector("#emails-view").style.display = 'none';
  document.querySelector("#show-mails-view").style.display = 'block';
}

archive_or_unarchive = (content) => {
  // archive/unarchive mails
  fetch(`emails/${content.id}`, {
    method: 'PUT',
    body : JSON.stringify({
      archived : !content.archived,
    })
  });
  // reload page
  location.reload()
}

reply_to_email = (sender, subject) => {
   // load compose view and set recipient and subject data
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#show-mails-view').style.display = 'none';
  document.querySelector('#email-options-view').style.display = 'none';
 
  document.querySelector("#compose-recipients").value = sender ;
  document.querySelector("#compose-subject").value = `Re: ${subject}`;
}

mark_as_read = content => {
  if (content.read === false){
    fetch(`/emails/${content.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }
}






