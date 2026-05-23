<script lang="js">
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
            formData.append('detail_level', detail.toString()); //no need for detail for now

            const response = await fetch('http://127.0.0.1:8000/documents/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Server Error' }));
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }

            const res = await response.json();
            apiResult = res.status || "File uploaded successfully!";

            const sumRes = await fetch('http://127.0.0.1:8000/documents/upload', {
                method: 'GET',
            });

            getSummary();
        } catch (error) {
            apiResult = error.message || "Something went wrong";
            console.error("Caught API Dropout:", errorMessage);
        } finally {
            isUploading = false;
            return
        }
    }

    async function getSummary() {
        try {
            const response = await fetch('http://127.0.0.1:8000/summaries', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error(errorData.detail || `Failed to get summaries: ${response.status}`);
            }

            const res = await response.json();
            summaryResult = res.message
        } catch (error) {
            apiResult = error.message || "Something went wrong";
            console.error("Caught API Dropout:", errorMessage);
        } finally {
            return
        }
    }

</script>

<div id="infer-box" class="main-box">
    <div id="infer-res">
        <h1>SUMMA AI</h1>
        {#if true}
        <p>Status: {apiResult}</p>
        <p>Inference result: {summaryResult}</p>
        {/if}
    </div>
    <div id="infer-button">
        <button onclick={uploadFile} class="sum-button">
            <b>Buat Rangkuman Dokumen</b>
        </button>
    </div>
</div>