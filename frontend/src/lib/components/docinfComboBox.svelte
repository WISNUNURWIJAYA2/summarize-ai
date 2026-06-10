<script lang="ts">
    import { fade } from 'svelte/transition';
    import {simulatedUpload} from '../../utils/mockAPI.js';
    import {uploadFile, getSummary} from '$lib/APIhelper.js';
    import { onMount } from 'svelte';
    
    let { files = $bindable([]), detail = $bindable(30), openDesc = $bindable(true)  } = $props();

    let debug = false;
    let apiResult = $state<any[]>([]);
    let summaryResult = $state<any[]>([]);
    let isUploading = $state(false);
    let uploadIndex  = $state<number>(-2);
    let copyIndex  = $state<number[]>([-1,-1]);
    let controller: AbortController | null = null;
    
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
            const currentFile : File = files[i]

            uploadIndex = i;

            controller = new AbortController();
            const { signal } = controller;
            try {
                const uploadString : string = await uploadFile(i,files,detail, signal);
                if (uploadString === "CANCELED") throw new Error("uploadCancel");
                apiResult.push({ 
                    filename: currentFile.name, 
                    status: uploadString 
                });
                const summaryString : string = await getSummary(i, signal);
                if (summaryString  === "CANCELED") throw new Error("summaryCancel");
                summaryResult.push({ 
                    filename: currentFile.name, 
                    summary: summaryString 
                });
            } catch (error) {
                if (error = "uploadCancel"){
                    apiResult.push({ 
                        filename: currentFile.name, 
                        status: "419" 
                    });
                }
                summaryResult.push({ 
                    filename: currentFile.name, 
                    summary: "Dibatalkan oleh pengguna." 
                });
            }
        };

        isUploading = false;
        controller = null;
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
        event.preventDefault();
        }
        
        fileInput.click();
    }

    async function copySummary(idx) {
        copyIndex = [1,idx]
        const textToCopy = summaryResult[idx].summary;
    
        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy);
            console.log("Copied to clipboard successfully!");
        } catch (err) {
            console.error("Failed to copy text: ", err);
    }
    }

    function downloadSingleSummary(idx: number) {
        copyIndex = [2,idx]
        
        const textToDownload = summaryResult[idx].summary;
    
        if (!textToDownload) return;

        const blob = new Blob([textToDownload], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        
        link.download = `summary_file_${files[idx].name}.txt`; 
        
        link.click();
        URL.revokeObjectURL(url);
    }

    function cancelUpload(){
        if (controller) {
        controller.abort();
        }
    }
    function resetFiles(){
        files = []
        apiResult = []
        summaryResult = []
        uploadIndex = -2
        copyIndex = [-1,-1]
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
    <div id="scroll-helper" class="flex relative flex-col flex-[4_0_0] justify-between overflow-y-auto">
        <div id = "document-info" class="flex flex-col flex-[1_0_0] justify-between">
            <button
                onclick={() => {openDesc = true}}
                class="md:hidden absolute top-1 right-4 text-2xl text-good-red"
            >
                <b>?</b>
            </button>
            <h1 class="text-4xl font-bold">SUMMA AI</h1>
                {#if debug == true}
                    {#if apiResult.length != 0}
                    <p>Status: {apiResult[0].status}</p>
                    {/if}
                {/if}
            <hr />
            <div id="doc-list" class="flex flex-1 flex-col md:flex-row">
                <label class="w-48 h-full md:min-h-0">
                    <input type="file" bind:files={curfile} bind:this={fileInput} onchange={handleFileSelection} accept=".pdf,.txt,.docx" style="display: none;"/>
                    <span class="sum-button" tabindex="0" role="button" onkeydown={triggerFileInput}>
                        <b>Pilih dokumen yang ingin diunggah</b>
                    </span>
                </label>
                <div id="doc-file-list" class="flex-1 h-18 overflow-y-auto h-4 md:h-full min-h-0 rounded-lg border-4 border-brand-color bg-brand-dark mx-2 px-2">
                    {#if files && files.length > 0}
                        {#each files as f}
                            <div class='flex justify-between even:bg-brand-darker odd:text-brand-lighter'>
                                <p class="truncate pr-4">{f.name}</p>
                                <p class="shrink-0 text-brand-unhigh">{Math.round(f.size / 1024**2)} MB</p>
                            </div>
                        {/each}
                        <button onclick={resetFiles} class="truncate w-full border-good-red! text-good-red! hover:bg-dark-red! active:hover:bg-dark-red!">
                            Batalkan pilihan
                        </button> 
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
        <div id = "inference-info" class="flex flex-col flex-[4_1_0] min-h-0 justify-between">
            <div id="infer-res" class="relative flex flex-col flex-1 min-h-0">
                {#if uploadIndex != -2}
                    <div id="infer-docs" class="flex-1 h-full min-h-0" in:fade={{duration:400,delay:100}} out:fade={{ duration: 50 }}>
                        {#each files as file,i}
                            <div id="doc-helper-{i}" in:fade={{duration:400,delay:200}} out:fade={{ duration: 25 }}>
                                {#if i > 0 && uploadIndex >= i}
                                    <hr  in:fade={{duration:200,delay:100}} out:fade={{ duration: 50 }}/>
                                {/if}
                                {#if isUploading && uploadIndex == i}
                                    <!-- Temporary file/uploading placeholder -->
                                    <div id="doc-{file.name}" class="flex flex-row h-full min-h-0" in:fade={{duration:200,delay:100}} out:fade={{ duration: 50 }}>
                                        <h2 class="w-4/5 min-h-0 truncate">
                                            {file.name}
                                        </h2>
                                        <button onclick={cancelUpload} class="sum-button w-2/5! md:w-1/5! py-0! border-good-red! text-good-red! hover:bg-dark-red! active:hover:bg-dark-red!">
                                            <b class="">Batalkan Unggahan</b>
                                        </button>
                                    </div>
                                    <p in:fade={{duration:200,delay:100}} out:fade={{ duration: 50 }} class="animate-pulse">File ini sedang diproses...</p>
                                {:else if uploadIndex >= i}
                                    <!-- Post upload / show summary -->
                                     <div id="doc-{file.name}" class="flex flex-row h-full min-h-0 truncate" in:fade={{duration:200,delay:100}} out:fade={{ duration: 50 }}>
                                        <h2 class="w-4/5 min-h-0 truncate">
                                            {summaryResult[i].filename}
                                        </h2>
                                        <button onclick={() => copySummary(i)} class="sum-button w-1/5! md:w-1/10! py-0!">
                                            <b class="">
                                                {copyIndex[0] === 1? copyIndex[1] === i? "Tersalin!" : "Salin" : "Salin"}
                                            </b>
                                        </button>
                                        <button onclick={() => downloadSingleSummary(i)} class="sum-button w-1/5! md:w-1/10! py-0!">
                                            <b class="">
                                                {copyIndex[0] === 2? copyIndex[1] === i? "Terunduh!" : "Unduh" : "Unduh"}
                                            </b>
                                        </button>
                                    </div>
                                    <p in:fade={{duration:100,delay:100}} out:fade={{ duration: 50 }}>{summaryResult[i].summary}</p>
                                {/if}
                            </div>
                        {/each}
                    </div>
                {:else}
                    <p in:fade={{duration:100,delay:100}} out:fade={{ duration: 100 }}>Upload file terlebih dahulu.</p>
                {/if}
            </div>
        </div>
    </div>
    <div id="infer-button" class="relative">
        <button onclick={handleUploads} class="sum-button">
            <b>Buat Rangkuman Dokumen</b>
        </button>
    </div>
</div>