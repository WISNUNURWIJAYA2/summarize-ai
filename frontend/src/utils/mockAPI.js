let simulatedDB = []

/**
 * @param {FileList | File[]} fileList 
 * @returns {Promise<{ result: string }>}
 */

export async function simulatedUpload(fileList) {
    await new Promise(resolve => setTimeout(resolve,1500))

    // Optional: Simulate random network dropouts (10% chance)
    if (Math.random() < 0.1) {
        throw new Error("500 Internal Server Error (Simulated)");
    }

    return {
        result: "Summary"
    }
}