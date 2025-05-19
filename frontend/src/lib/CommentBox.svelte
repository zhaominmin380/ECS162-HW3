<script>
    import Reply from './Reply.svelte';

    export let article;
    export let onClose;

    let comments = [];
    let content = '';
    let reply = null;

    // nested comment algo
    function nestComments(comments) {
        const map = {};
        const roots = [];

        comments.forEach(c => {
            c.children = [];
            map[String(c._id)] = c;
        });

        comments.forEach(c => {
            let pid;
            if (c.parent_id) {
              pid = String(c.parent_id);
            } else {
              pid = undefined;  
            }
            if (pid && map[pid]) {
                map[pid].children.push(c);
            } else {
                roots.push(c);
            }
        });

        return roots;
    }

    // count both comment and reply
    function countAll(comments) {
        let count = 0;
        for (const c of comments) {
            count += 1;
            if (c.children?.length) {
                count += countAll(c.children);
            }
        }
        return count;
    }

    // get comment already in article
    async function fetchComments() {
        const res = await fetch(`/api/comments?article_url=${encodeURIComponent(article.url)}`);
        let flat;
        if (res.ok) {
          flat = await res.json();
        } else {
          flat = [];
        }
        comments = nestComments(flat);
        //console.log('nesting:', nestComments(flat));
    }

    // submit comment or reply
    async function submitComment(parentId, content) {
            const res = await fetch('/api/comments', {
            method: 'POST',
            credentials: 'include',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                article_url: article.url,
                content: content,
                parent_id: parentId
            })
        });
        if (res.ok) {
            reply = null;
            fetchComments();
        }else{
          const err = await res.json();
          alert(err?.error);
        }
    }
   
    // delete comment (moderator  only)
    async function deleteComment(id) {
        const res = await fetch(`/api/comments/${id}`, { method: 'DELETE' });
        if (res.ok){
          fetchComments();
        }else{
          const err = await res.json();
          alert(err?.error);
        }
    }

    // refresh when different article
    $: if (article) {
        fetchComments(); 
    }

    function setReply(id) {
        reply = id;
    }

</script>

<div class="sidebar">
  <div class="sidebar-header">
    <h2>{article?.headline}</h2>
    <button on:click={onClose}>✕</button>
  </div>

  <div class="sidebar-comments">
    <h3>Comments <span>{countAll(comments)}</span></h3>

    <!-- comment byself -->
    {#if !reply}
        <input type="text" placeholder="Share your thoughts..." bind:value={content} />
        <div class="button">
          <button on:click={() => {submitComment(null, content); content="";}}>Send</button>
        </div>
    {/if}

    <!-- nested comment -->
    {#each comments as c}
        <Reply
            comment={c}
            {reply}
            {setReply}
            {submitComment}
            {deleteComment}
        />
    {/each}

  </div>
</div>

<style>
  .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 350px;
    height: 100%;
    background: white;
    box-shadow: -2px 0 8px rgba(0,0,0,0.15);
    z-index: 999;
    display: flex;
    flex-direction: column;
    padding: 20px;
    overflow-y: auto;
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
  }

  .sidebar-comments h3 {
    margin-top: 20px;
  }

  .sidebar-comments input {
    display:flex;
    justify-content: center;
    width: 90%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
  }

  .button {
    display:flex;
    justify-content: flex-end;
  }

  .button > button{
    font-size:0.7em;
  }

</style>
