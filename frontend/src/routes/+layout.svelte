<script lang="ts">
	import axios from 'axios';
	let { children } = $props();
</script>


<nav class="hidden absolute bg-black w-full h-[10%]">
	<ul class="flex flex-row justify-around">
		<li>Document</li>
		<li>Dicument</li>
		<li>Ducument</li>
		<li>Dacument</li>
		<li>Decument</li>
	</ul>
</nav>

{@render children()}