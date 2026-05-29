<script lang="js">
	import axios from 'axios';
    import {simulatedUpload} from '../../utils/mockAPI.js';

    let debug = false;
    let apiResult = $state([]);
    let summaryResult = $state([]);
    let isUploading = $state(false);

    let { files = $bindable([]), detail = $bindable(10) } = $props();

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
            formData.append('detail_level', detail); //no need for detail for now
            
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

</script>


<div id="infer-box" class="main-box flex flex-col flex-[3_1_0] justify-between">
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