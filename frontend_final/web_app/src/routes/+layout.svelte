<script>
  import favicon from "$lib/assets/favicon.svg";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<nav>
  <a href="/">หน้าหลัก</a>
  <a href="/parties">ข้อมูลพรรคการเมือง</a>
  <a href="/voters">ผู้มีสิทธิเลือกตั้ง</a>
  <a href="/voting">บันทึกการลงคะแนน</a>
  <a href="/results">รายงานผลการเลือกตั้ง</a>
</nav>

{@render children()}

<style>
  nav {
    padding: 1rem;
    background: #f8f9fa;
    border-bottom: 2px solid #ddd;
    margin-bottom: 2rem;
  }
  nav a {
    margin: 0 10px;
    text-decoration: none;
    color: #333;
    font-weight: bold;
  }
  nav a:hover {
    color: #007bff;
  }
</style>
