<script lang="js">
    let title = "Tailwind com @apply no Svelte!";
</script>

<div class="container">
    <h1 class="title">{title}</h1>
    <button class="button">Clique Aqui</button>
</div>

<style>
    .container {
        @apply flex flex-col items-center justify-center h-screen bg-gray-100;
    }

    .title {
        @apply text-3xl font-bold text-blue-600;
    }

    .button {
        @apply mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700;
    }
</style>
