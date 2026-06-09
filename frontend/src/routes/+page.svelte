<script lang="ts">
    
	import DocumentBox from '$lib/components/documentBox.svelte';
	import InferBox from '$lib/components/inferenceBox.svelte';
	import ComboBox from '$lib/components/docinfComboBox.svelte';
	import DescBox from '$lib/components/descriptionBox.svelte';

    let files = $state<File[]>([]);
    let detail = $state(0);

    let openDesc = $state(true);
</script>

<style>
@import '../app.css';
</style>

<div id='main-app' class="max-md:absolute md:flex md:flex-row justify-around max-md:w-full h-screen max-md:px-2 overflow-visible md:gap-2">
    <ComboBox bind:files={files} bind:detail={detail} bind:openDesc={openDesc} />
    <DescBox bind:openDesc={openDesc}/>
</div>
