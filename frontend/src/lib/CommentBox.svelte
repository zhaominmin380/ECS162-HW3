<script>
    import Reply from './Reply.svelte';

    export let article;
    export let onClose;

    let comments = [];
    let content = '';
    let reply = null;
    
    function nestComments(comments) {
        const map = {};
        const roots = [];

        comments.forEach(c => {
            c.children = [];
            map[String(c._id)] = c;
        });

        comments.forEach(c => {
            const pid = c.parent_id && String(c.parent_id);
            if (pid && map[pid]) {
                map[pid].children.push(c);
            } else {
                roots.push(c);
            }
        });

        return roots;
    }

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

    async function fetchComments() {
        const res = await fetch(`/api/comments?article_url=${encodeURIComponent(article.url)}`);
        const flat = res.ok ? await res.json() : [];
        comments = nestComments(flat);
        console.log('nesting:', nestComments(flat));
    }

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
        }
    }

    async function deleteComment(id) {
        const res = await fetch(`/api/comments/${id}`, { method: 'DELETE' });
        if (res.ok) fetchComments();
    }

    $: if (article) {
        fetchComments(); 
    }

    function setReply(id) {
        reply = id;
    }

    function setContent(val) {
        content = val;
    }

</script>

<div class="sidebar">
  <div class="sidebar-header">
    <h2>{article?.headline}</h2>
    <button on:click={onClose}>✕</button>
  </div>

  <div class="sidebar-comments">
    <h3>Comments <span>{countAll(comments)}</span></h3>

    {#if !reply}
        <input type="text" placeholder="Share your thoughts..." bind:value={content} />
        <button on:click={() => submitComment(null)}>Send</button>
    {/if}
    {#each comments as c}
        <Reply
            comment={c}
            {reply}
            {setReply}
            {submitComment}
            {deleteComment}
            {content}
            {setContent}
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
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
  }

  .comment {
    margin-bottom: 12px;
    padding: 6px;
    border-bottom: 1px solid #eee;
  }

  .comment .delete {
    font-size: 12px;
    color: blue;
    background: none;
    border: none;
    cursor: pointer;
  }
</style>
