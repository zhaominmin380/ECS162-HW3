<script>
  let todayDate = new Date().toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  let news = []; 
  // fetch data
  fetch('/api/news')
    .then(response => response.json())
    .then(data => {
      news = data;
    })
    .catch(error => {
      console.error('Error fetching news:', error);
    });

  //'/api/comments', POST, testing
  let content = '';
  let articleUrl = 'https://example.com/test-article'; 
  let result = '';

  async function submitComment() {
    const res = await fetch('/api/comments', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        article_url: articleUrl,
        content: content,
        parent_id: null
      })
    });

    if (res.ok) {
      const data = await res.json();
      result = 'sucess：' + data._id;
      content = '';
    } else {
      const err = await res.json();
      result = 'error：' + (err.description || JSON.stringify(err));
    }
  }

  // GET testing
  let comments = [];
  let commentsError = '';
  let deleteResult = '';

  async function fetchComments() {
    commentsError = '';
    try {
      const res = await fetch(`/api/comments?article_url=${encodeURIComponent(articleUrl)}`);
      if (res.ok) {
        comments = await res.json();
      } else {
        const err = await res.json();
        commentsError = err.error || JSON.stringify(err);
      }
    } catch (err) {
      commentsError = 'Network error: ' + err.message;
    }
  }

  // Delete testing
  async function deleteComment(id) {
    deleteResult = '';
    try {
      const res = await fetch(`/api/comments/${id}`, {
        method: 'DELETE'
      });

      if (res.ok) {
        fetchComments();
      } else {
        const err = await res.json();
        deleteResult = 'Error deleting: ' + (err.error || JSON.stringify(err));
      }
    } catch (err) {
      deleteResult = 'Network error: ' + err.message;
    }
  }

  //login function
    let user = null;

  fetch('/api/user') 
    .then(res => res.ok ? res.json() : null)
    .then(data => {
      user = data?.user ?? null;
    });

  function login() {
    window.location.href = 'http://localhost:8000/login';
  }

  function logout() {
    window.location.href = 'http://localhost:8000/logout';
  }
</script>

<!-- Header -->
<div class="frame">
  <div class="date">
    {todayDate}<br />Today's Paper
  </div>          
  <div class="title">
    <img src="/logo.png" alt="NYT Logo">
  </div>
  <div class="right">
    <div id="auth-area">
      {#if user}
        <div class="user-info">
          {user.email}
          <button on:click={logout}>Log out</button>
        </div>
      {:else}
        <button on:click={login}>Log in</button>
      {/if}
    </div>
  </div>  
</div>

<!-- Main Grid Container -->
<div class="main">
  
  <!-- Left Top Column -->
  <div class="left-col">
    {#if news.length > 0}
      {#if news[0].image}
        <img src={news[0].image} alt="news image">
      {/if}
      <article>
        <h2>{news[0].headline}</h2>
        <p>{news[0].abstract || news[0].snippet}</p>
        <a href={news[0].url} target="_blank">Read more</a>
      </article>

      <!-- testing -->
      <div class="comment-box">
      <h3>test comments</h3>
        <textarea bind:value={content} placeholder="Enter..."></textarea>
        <button on:click={submitComment}>send</button>
        {#if result}
          <p>{result}</p>
        {/if}
        <button on:click={fetchComments}>Get Comments</button>
        {#if deleteResult}
          <p style="color: green;">{deleteResult}</p>
        {/if}

        {#if commentsError}
          <p style="color: blue;">{commentsError}</p>
        {/if}
        <ul>
          {#each comments as c}
            <li>{c.content}</li>
            <button on:click={() => deleteComment(c._id)}>Delete</button>
          {/each}
        </ul>
      </div>
    {/if}
    <hr/>
  </div>

  <!-- Left Bottom Column -->
  <div class="left1-col">
    {#if news.length > 1}
      {#if news[1].image}
        <img src={news[1].image} alt="news image">
      {/if}
      <article>
        <h2>{news[1].headline}</h2>
        <p>{news[1].abstract || news[1].snippet}</p>
        <a href={news[1].url} target="_blank">Read more</a>
      </article>
    {/if}
    <hr/>
  </div>

  <!-- Middle Top Column -->
  <div class="middle-col">
    {#if news.length > 2}
      {#if news[2].image}
        <img src={news[2].image} alt="news image">
      {/if}
      <article>
        <h2>{news[2].headline}</h2>
        <p>{news[2].abstract || news[2].snippet}</p>
        <a href={news[2].url} target="_blank">Read more</a>
      </article>
    {/if}
    <hr/>
  </div>

  <!-- Middle Bottom Column -->
  <div class="middle1-col">
    {#if news.length > 3}
      {#if news[3].image}
        <img src={news[3].image} alt="news image">
      {/if}
      <article>
        <h2>{news[3].headline}</h2>
        <p>{news[3].abstract || news[3].snippet}</p>
        <a href={news[3].url} target="_blank">Read more</a>
      </article>
    {/if}
    <hr/>
  </div>

  <!-- Right Top Column -->
  <div class="right-col">
    {#if news.length > 4}
      {#if news[4].image}
        <img src={news[4].image} alt="news image">
      {/if}
      <article>
        <h2>{news[4].headline}</h2>
        <p>{news[4].abstract || news[4].snippet}</p>
        <a href={news[4].url} target="_blank">Read more</a>
      </article>
    {/if}
    <hr/>
  </div>

  <!-- Right Bottom Column -->
  <div class="right1-col">
    {#if news.length > 5}
      {#if news[5].image}
        <img src={news[5].image} alt="news image">
      {/if}
      <article>
        <h2>{news[5].headline}</h2>
        <p>{news[5].abstract || news[5].snippet}</p>
        <a href={news[5].url} target="_blank">Read more</a>
      </article>
    {/if}
    <hr/>
  </div>

</div>

<hr/>

<style>
.frame{
    display:flex;
    align-items: center;
    max-width:1400px;
    margin:auto;
    margin-bottom: 10px;
    border-bottom: 1px solid #ccc;
}
.date {
    flex:1;
    padding: 20px;
    text-align: left;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.title {
    flex:1;
    padding: 20px;
    text-align: center;
}

.title img {
    height:80px;
}
/* blank so title will be in center*/
.right {
    flex:1;
    display:flex;
    justify-content: flex-end;
}

#auth-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* grid container*/
.main {
    display:grid;
    grid-template-areas: 
        'l1  m1 m1 r1'
        'l2  m2 m2 r2';
    max-width: 1400px;
    margin: auto;
}

.left-col,
.left1-col,
.middle-col,
.middle1-col,
.right-col,
.right1-col{
    padding: 20px;
    margin-left: 20px;
    font-family: Georgia;
}

.left-col{
    text-align: left;
    grid-area:l1;
}

.left1-col{
    text-align: left;
    grid-area:l2;
}

.left-col img {
    width:100%;
    height:auto;
}

.left1-col img {
    width:100%;
    height:auto;
}

.middle-col{
    text-align: left;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
    grid-area:m1;
    
}

.middle-col img {
    width:100%;
    height:300px;
}

.middle1-col{
    text-align: left;;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
    grid-area:m2;
    
}

.middle1-col img {
    width:100%;
    height:300px;
}

.right-col{
    text-align: left;
    grid-area:r1;
}

.right1-col{
    text-align: left;
    grid-area:r2;
}

.right-col img {
    width:100%;
    height:auto;
}

.right1-col img {
    width:100%;
    height:auto;
}

hr {
    height: 1px;
    background-color: #ccc;
    border: none;
    max-width:1400px;
    margin: auto;
    margin-top:20px;
}

/* 2 columns (786-1024)*/
@media (max-width:1024px) {
    .main {
        display:grid;
        grid-template-areas: 
            'm1 m1 l1'
            'm2 m2 r1'
            '. . l2'
            '. . r2';
        margin: auto;
    }

    .middle-col{
        text-align: left;
        border:none;
        grid-area:m1;
        
    }
    
    .middle1-col{
        text-align: left;
        border:none;
        grid-area:m2;
        
    }

    .left-col{
        text-align: left;
        border-left: 1px solid #ccc;
        grid-area:l1;
    }
    
    .left1-col{
        text-align: left;
        border-left: 1px solid #ccc;
        grid-area:l2;
    }

    .right-col{
        text-align: left;
        border-left: 1px solid #ccc;
        grid-area:r1;
    }
    
    .right1-col{
        text-align: left;
        border-left: 1px solid #ccc;
        grid-area:r2;
    }
    
}

/* 1 columns (< 786)*/
@media (max-width:768px) {
    .main {
        display:grid;
        grid-template-areas: 
            'm1'
            'm2'
            'l1'
            'l2'
            'r1'
            'r2';
        margin: auto;
    }

    .left-col,
    .left1-col,
    .right-col,
    .right1-col{
        border:none;
    }
}
</style>