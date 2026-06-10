import axios from 'axios';
import { get } from 'node:http';

const client = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    timeout: 60000, // 60-second timeout for heavy ML workloads
});

export async function uploadFile(index: number,files: File[],detail: number = 50, signal?: AbortController){
    try {
        const fileToUpload = files[index];
        const formData = new FormData();
        formData.append('file', fileToUpload);
        formData.append('ratio', detail.toString()); //no need for detail for now
        
        let uploadEndpoint = '/documents/upload';
        let parseEndpoint = '/documents/parse';
        const res = await client.post(uploadEndpoint, formData, {
            signal,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        
        return res.status.toString() || "File uploaded successfully!";
    } catch (error: any) {
        if (axios.isCancel(error)) {
            return "CANCELED";
        }
        console.error("Caught API Dropout:", error.message);
        return error.message || "Something went wrong";
    }
}




export async function getSummary(index: number, signal?: AbortController) {
    try {
        let summaryEndpoint = 'http://127.0.0.1:8000/summaries/';
        const res = await axios.get(summaryEndpoint, { signal })
        console.log(res)
        return res.data.message
    } catch (error: any) {
        if (axios.isCancel(error)) {
            return "CANCELED"; // Return a specific string if intentionally aborted
        }
        console.error("Caught API Dropout:", error.message);
        return "Error: " + error.message || "Something went wrong";
    }
}
