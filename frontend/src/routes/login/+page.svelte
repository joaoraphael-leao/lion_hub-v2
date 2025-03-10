<script>
    import { goto } from "$app/navigation";
    
    let email = "";
    let password = "";
    
    async function handleSubmit(event) {
        event.preventDefault();
        console.log("Form submitted");  // Debug log
        
        try {
            // Adicione sua lógica de autenticação aqui
            console.log("Login attempt:", { email, password });
            return false; // Explicitly return false to prevent form submission
        } catch (error) {
            console.error("Login error:", error);
        }
    }
</script>

<div class="login-container">
    <h1>Login</h1>
    <form 
        on:submit|preventDefault={handleSubmit}
        method="POST"
        action=""
    >
        <div class="form-group">
            <label for="email">Email:</label>
            <input 
                type="email" 
                id="email" 
                bind:value={email} 
                required
            />
        </div>
        
        <div class="form-group">
            <label for="password">Senha:</label>
            <input 
                type="password" 
                id="password" 
                bind:value={password} 
                required
            />
        </div>
        
        <button type="submit">Entrar</button>
    </form>
</div>

<style>
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        border: 1px solid #ccc;
        border-radius: 8px;
    }
    
    .form-group {
        margin-bottom: 1rem;
    }
    
    label {
        display: block;
        margin-bottom: 0.5rem;
    }
    
    input {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    
    button {
        width: 100%;
        padding: 0.75rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    button:hover {
        background-color: #45a049;
    }
</style>