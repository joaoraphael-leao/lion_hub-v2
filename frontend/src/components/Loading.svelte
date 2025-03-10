<script>
  import { onMount } from "svelte";
  import { goto } from "$app/navigation"; // Para redirecionamento no SvelteKit

  // Redireciona para a página de login após 3 segundos
  onMount(() => {
    setTimeout(() => {
      goto("/"); // Alterar para a rota correta do login
    }, 10000);
  });
</script>

<style>

  /* Estilização do fundo e centralização */
  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #0044cc;
      margin: 0/* Cor de fundo azul */
  }

  /* Estilização do ícone do leão */
  .lion-icon {
    width: 150px; /* Tamanho do ícone */
    height: 150px;
    animation: fadeIn 2.6s ease-in-out;
  }

  /* Efeito de fade-in */
  @keyframes fadeIn {
    from {
      opacity: 0.2;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1.2);
    }
  }
</style>

<!-- 🔹 Estrutura HTML do componente -->
<div class="loading-container">
  <img class="lion-icon" src="/lion.png" alt="Leão">
</div>