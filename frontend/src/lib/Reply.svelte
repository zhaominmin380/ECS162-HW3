<script>
  import Reply from './Reply.svelte';
  
  export let comment;
  export let reply;
  export let setReply;
  export let submitComment;
  export let deleteComment;
  let localContent = "";
  console.log('render:', comment);
  console.log("Replying to:", comment._id);
</script>

<div class="comment">
  <strong>{comment.username || 'Anonymous'}</strong>
  <p>{comment.content}</p>
  <button on:click={() => setReply(comment._id)}>Reply</button>
  <button on:click={() => deleteComment(comment._id)}>Delete</button>

  {#if reply === comment._id}
    <div class="reply-box">
      <input type="text" placeholder="Write a reply..." bind:value={localContent} />
      <button on:click={() => {
        submitComment(comment._id, localContent);
        localContent = "";}}>Send</button>
    </div>
  {/if}

  <div class="replies">
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
  .replies {
    margin-left: 20px;
    border-left: 1px solid #ccc;
    padding-left: 10px;
  }
  .reply-box {
    margin-top: 5px;
  }
</style>
