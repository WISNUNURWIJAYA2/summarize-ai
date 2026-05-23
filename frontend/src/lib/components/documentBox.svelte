<script lang="ts">
    import { onMount } from 'svelte';
    
    

    let { files = $bindable([]), detail = $bindable(10) } = $props();

    let curfile  = $state<FileList|undefined>(undefined);
    let fileInput = $state<HTMLInputElement | undefined>(undefined);
    let min,max,step;
    min = 10
    max = 90
    step = 1
    
    onMount(() => {
        if (fileInput) {
            fileInput.value = '';
        }
        curfile = undefined;
    });
    
    function handleFileSelection(event: Event) {
        if (curfile && curfile.length > 0) {       
            files = [...files, ...Array.from(curfile)];
            
            if (fileInput) fileInput.value = '';
            curfile = undefined;
        }
    }

    function yoho() {
        console.log(files)
        return
    }
</script>


<div id="doc-box" class="main-box">
    <div id="doc-list">
        <label>
            <input type="file" bind:files={curfile} bind:this={fileInput} onchange={handleFileSelection} accept=".pdf,.txt,.docx" style="display: none;"/>
            <span class="sum-button"><b>Unggah dokumen di sini</b></span>
        </label>
        <div id="doc-file-list">
        
            {#if files && files.length > 0}
                {#each files as f}
                    <p>{f.name}</p>
                    <p>{Math.round(f.size / 1024**2)} MB</p>
                {/each}
            {:else}
                <p>Tidak ada file tersimpan.</p>
            {/if}
        </div>
    </div>
    <div id="doc-pow-slider">
            <p><b>Tingkat Detail:</b> {detail}%</p>
            <input 
                type="range" 
                {min} 
                {max} 
                {step}
                bind:value={detail} 
                class="custom-slider"
            />
    </div>
</div>