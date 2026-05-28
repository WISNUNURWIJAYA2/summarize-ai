<script lang="js">
	import axios from 'axios';
    import {simulatedUpload} from '../../utils/mockAPI.js';

    let apiResult = $state("Test");
    let summaryResult = $state("Test");
    let isUploading = $state(false);

    let { files = $bindable([]), detail = $bindable(10) } = $props();

    async function uploadFile() {
        if (files.length === 0) return;
        try {

            isUploading = true;
            /* Testing simulated
            const res = await simulatedUpload(files);
            */

            const fileToUpload = files[0];
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
            
            apiResult = res.status.toString() || "File uploaded successfully!";

            getSummary();
        } catch (error) {
            apiResult = error.message || "Something went wrong";
            console.error("Caught API Dropout:", error.message);
        } finally {
            isUploading = false;
            return
        }
    }

    async function getSummary() {
        try {
            let summaryEndpoint = 'http://127.0.0.1:8000/summaries/';
            const res = await axios.get(summaryEndpoint)

            summaryResult = res.data.message
            console.log(res)
        } catch (error) {
            summaryResult = error.message || "Something went wrong";
            console.error("Caught API Dropout:", errorMessage);
        } finally {
            return
        }
    }

</script>

<div id="infer-box" class="main-box flex flex-col flex-[3_1_0] justify-between">
    <div id="infer-res">
        <h1 class="text-4xl font-bold">SUMMA AI</h1>
        {#if true}
        <p>Status: {apiResult}</p>
        <p>Inference result: {summaryResult}</p>
        {/if}
    </div>
    <div id="infer-button" class="relative">
        <button onclick={uploadFile} class="sum-button">
            <b>Buat Rangkuman Dokumen</b>
        </button>
    </div>
</div>