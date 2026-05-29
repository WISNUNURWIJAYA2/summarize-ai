<script lang="ts">
    import { onMount } from 'svelte';
    
    

    let { files = $bindable([]), detail = $bindable(30) } = $props();

    let curfile  = $state<FileList|undefined>(undefined);
    let fileInput = $state<HTMLInputElement | undefined>(undefined);
    let min,max,step;
    min = 30
    max = 70
    step = 20
    let barColor = $state("#000000")
    
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

    function triggerFileInput(event: MouseEvent | KeyboardEvent) {
        if (event.type === 'keydown') {
        const keyEvent = event as KeyboardEvent;
        if (keyEvent.key !== 'Enter' && keyEvent.key !== ' ') return;
        event.preventDefault(); // Stop page from scrolling on Spacebar
        }
        
        fileInput.click();
    }

    $effect(() => {
        if (detail == 70){
            detail = 80;
        }
        calcLen();
    })

    function calcLen() {
        if(detail == 30){barColor = "#100520"}
        else if(detail == 50){barColor = "#3060b0"}
        else if(detail == 80){barColor = "#80bbff"}
        else {barColor = "#100520"}
    }
</script>


<div id="doc-box" class="main-box flex flex-col flex-1 justify-between">
    <div id="doc-list">
        <label class="w-full">
            <input type="file" bind:files={curfile} bind:this={fileInput} onchange={handleFileSelection} accept=".pdf,.txt,.docx" style="display: none;"/>
            <span class="sum-button" tabindex="0" role="button" onkeydown={triggerFileInput}>
                <b>Unggah dokumen di sini</b>
            </span>
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
    <div id="doc-pow-slider" class="relative w-full">
            <p><b>Tingkat Detail:</b> {detail}%</p>
            <input 
                type="range" 
                {min} 
                {max} 
                {step}
                bind:value={detail} 
                class="custom-slider w-full border-4 border-brand-dark2 rounded-xl py-2 overflow-visible"
                style="--dynamic-track-color: {barColor};"
            />
    </div>
</div>