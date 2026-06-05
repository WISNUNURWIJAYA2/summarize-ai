<script lang="ts">
	import axios from 'axios';
    import {simulatedUpload} from '../../utils/mockAPI.js';
    import { onMount } from 'svelte';
    
    let { files = $bindable([]), detail = $bindable(10) } = $props();

    let debug = false;
    let apiResult = $state([]);
    let summaryResult = $state([]);
    let isUploading = $state(false);

    let curfile  = $state<FileList|undefined>(undefined);
    let fileInput = $state<HTMLInputElement | undefined>(undefined);
    let min,max,step;
    min = 30
    max = 70
    step = 20
    let barColor = $state("#000000")

    async function handleUploads() {
        if (files.length === 0) return;

        isUploading = true;

        apiResult = [];
        summaryResult = [];

        for (let i = 0; i < files.length; i++) {
            const currentFile = files[i]

            const uploadString = await uploadFile(i);
            apiResult.push({ 
                filename: currentFile.name, 
                status: uploadString 
            });
            const summaryString = await getSummary();
            summaryResult.push({ 
                filename: currentFile.name, 
                summary: summaryString 
            });
        };

        isUploading = false;
    }

    async function uploadFile(index){
        try {
            const fileToUpload = files[index];
            const formData = new FormData();
            formData.append('file', fileToUpload);
            formData.append('ratio', detail); //no need for detail for now
            
            let uploadEndpoint = 'http://127.0.0.1:8000/documents/upload';
            let parseEndpoint = 'http://127.0.0.1:8000/documents/parse';
            const res = await axios.post(uploadEndpoint, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            
            return res.status.toString() || "File uploaded successfully!";
        } catch (error) {
            console.error("Caught API Dropout:", error.message);
            return error.message || "Something went wrong";
        }
    }

    async function getSummary() {
        try {
            let summaryEndpoint = 'http://127.0.0.1:8000/summaries/';
            const res = await axios.get(summaryEndpoint)

            console.log(res)
            return res.data.message
        } catch (error) {
            console.error("Caught API Dropout:", errorMessage);
            return error.message || "Something went wrong";
        }
    }
    
    
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

    function barColorize() {
        if(detail == 30){barColor = "#100520"}
        else if(detail == 50){barColor = "#3060b0"}
        else if(detail == 80){barColor = "#80bbff"}
        else {barColor = "#100520"}
    }

    onMount(() => {
        if (fileInput) {
            fileInput.value = '';
        }
        curfile = undefined;
    });

    $effect(() => {
        if (detail == 70){
            detail = 80;
        }
        barColorize();
    }) 
</script>

<div id="combo-box" class="main-box flex flex-col flex-[4_0_0] justify-between">
    <div id = "document-info" class="flex flex-col flex-[1_0_0] justify-between">
        <div id="doc-list" class="flex flex-1 flex-row">
            <label class="w-48 h-full min-h-0">
                <input type="file" bind:files={curfile} bind:this={fileInput} onchange={handleFileSelection} accept=".pdf,.txt,.docx" style="display: none;"/>
                <span class="sum-button" tabindex="0" role="button" onkeydown={triggerFileInput}>
                    <b>Unggah dokumen di sini</b>
                </span>
            </label>
            <div id="doc-file-list" class="flex-1 h-18 overflow-y-auto min-h-0 rounded-lg border-4 border-brand-color bg-brand-dark mx-2 px-2">
                {#if files && files.length > 0}
                    {#each files as f}
                        <div class='flex justify-between even:bg-brand-darker odd:text-brand-lighter'>
                            <p class="truncate pr-4"><bold>{f.name}</bold></p>
                            <p class="shrink-0 text-brand-unhigh">{Math.round(f.size / 1024**2)} MB</p>
                        </div>
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
    <hr>
    <div id = "inference-info" class="flex flex-col flex-[4_1_0] justify-between">
        <div id="infer-res">
        <h1 class="text-4xl font-bold">SUMMA AI</h1>
        {#if debug == true}
        <p>Status: {apiResult}</p>
        {/if}
        {#if summaryResult.length > 0}
            {#each summaryResult as sum}
                <hr>
                <h2>{sum.filename}</h2>
                <p>{sum.summary}</p>
            {/each}
        {:else}
            <hr>
            <p>Upload file terlebih dahulu.</p>
        {/if}
    </div>
    <div id="infer-button" class="relative">
        <button onclick={handleUploads} class="sum-button">
            <b>Buat Rangkuman Dokumen</b>
        </button>
    </div>
    </div>
</div>