<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import Loading from "/src/components/Loading.svelte";

  onMount(() => {
    setTimeout(() => {
      goto("/login"); // Altere para a rota correta do login
    }, 2000); // Tempo de carregamento (5 segundos)
  });
</script>

<Loading/>