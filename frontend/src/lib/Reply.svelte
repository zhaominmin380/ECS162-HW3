<script>
  import Reply from './Reply.svelte';
  
  export let comment;
  export let reply;
  export let setReply;
  export let submitComment;
  export let deleteComment;
  let localContent = "";
  //console.log('render:', comment);
  //console.log("Replying to:", comment._id);
</script>

<div class="comment">
  <strong>{comment.username}</strong>
  <p>{comment.content}</p>
  <div class="button">
    <button on:click={() => setReply(comment._id)}>Reply</button>
    <button on:click={() => deleteComment(comment._id)}>Delete</button>
  </div>

  {#if reply === comment._id}
    <div class="reply-box">
      <!-- reply to someone -->
      <input type="text" placeholder="Write a reply..." bind:value={localContent} />
      <button on:click={() => {submitComment(comment._id, localContent);localContent = "";}}>Send</button>
    </div>
  {/if}

  <div class="replies">
    <!-- loop through all childrens -->
    {#each comment.children as child}
      <Reply
        comment={child}
        {reply}
        {setReply}
        {submitComment}
        {deleteComment}
      />
    {/each}
  </div>
</div>

<style>
  .comment {
    margin-bottom: 12px;
    padding: 6px;
    border-bottom: 1px solid #eee;
  }

  .button {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    font-size: 0.5em;
    margin-bottom: 8px;
  }

  .replies {
    margin-left: 20px;
    border-bottom: none;
    border-left: 1px solid #ccc;
    padding-left: 10px;
  }

  .reply-box input{
    margin-top: 5px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
  }
</style>
