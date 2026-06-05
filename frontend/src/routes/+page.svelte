<script lang="ts">
    
	import DocumentBox from '$lib/components/documentBox.svelte';
	import InferBox from '$lib/components/inferenceBox.svelte';
	import ComboBox from '$lib/components/docinfComboBox.svelte';
	import DescBox from '$lib/components/descriptionBox.svelte';

    let files = $state<File[]>([]);
    let detail = $state(0);

    let mobile = $state(true); //figure out how to store variables
</script>

<style>
@import '../app.css';
</style>

<div id='main-app' class="flex flex-row justify-around w-full h-[90vh] gap-2">
    <ComboBox bind:files={files} bind:detail={detail} />
    <DescBox />
</div>
