<script lang="ts">
    
	import DocumentBox from '$lib/components/documentBox.svelte';
	import InferBox from '$lib/components/inferenceBox.svelte';
	import DescBox from '$lib/components/descriptionBox.svelte';

    let files = $state<File[]>([])
    let detail = $state(0);

    let mobile = false; //figure out how to store variables
</script>

<style>
@import '../app.css';
</style>

<div id='main-app'>
    <DocumentBox bind:files={files} bind:detail={detail} />
    <InferBox bind:files={files} bind:detail={detail}/>
    <DescBox />
</div>
