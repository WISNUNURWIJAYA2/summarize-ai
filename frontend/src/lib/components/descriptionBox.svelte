<script lang="ts">
    let { mobile = $bindable(false), openDesc = $bindable(false)} = $props();
    let position = $state<string>("0");
    $effect(() => {
        if (openDesc == true){
            position = "0";
        } else {
            position = "100vw"
        }
    });
</script>


<div id="desc-box" class="main-box transition-transform max-md:absolute max-md:top-0 translate-x-(--dynamic-left) max-md:w-[99vw]! md:translate-x-0 md:flex-1" style="--dynamic-left: {position};">
    <button
        onclick={() => {openDesc = false}}
        class="md:hidden absolute top-1 right-4 text-2xl text-good-red"
    >
        <b>X</b>
    </button>
    <div id="web-info">
        <h2>SUMMA AI</h2>
    </div>
    <hr>
    <div id="instructions-info">
        <h2>Instruksi</h2>
        <ol>
            <li>Pilih file yang ingin diunggah.</li>
            <li>Tentukan level detail yang diinginkan menggunakan slider.</li>
            <li>Tekan tombol "Buat Rangkuman di bagian bawah layar".</li>
            <li>Tunggu hasil rangkuman.</li>
            <li>Untuk menyalin atau mengunduh hasil, dapat menekan tombol di samping judul file.</li>
        </ol>
    </div>
    <hr>
    <div id="tech-info">
        <h2>Teknologi</h2>
        <p>Kami menggunakan LangChain untuk membuat rangkuman teks dari dokumen yang diberikan. Menggunakan slider, Anda dapat mengatur tingkat detail pada hasil rangkuman.</p>
        <p class="TEMP hidden">Tolong bantu isi sisanya.</p>
    </div>
    <hr>
    <div id="team-info">
        <h2>Tim</h2>
        <p>Tim kami terdiri dari 5 orang anggota. Proyek ini dibangun sebagai salah satu syarat kelulusan program Pijak in collaboration with IBM Skillbuild</p>
        <hr>
        <ul>
            <li><b>Mohamad Rizki:</b> Berasal dari Politeknik Negeri Indramayu. Berperan mengembangkan model untuk merangkum teks.</li>
            <li><b>M. Fadil Faiz:</b> Berasal dari Politeknik Negeri Indramayu. Berperan mengembangkan model untuk merangkum teks.</li>
            <li><b>Ibrahim Movik:</b> Berasal dari Politeknik Negeri Indramayu. Berperan mengembangkan model untuk merangkum teks.</li>
            <li><b>Wisnu Nur Wijaya:</b> Berasal dari STIKOM POLTEK CIREBON. Berperan merancang backend aplikasi.</li>
            <li><b>Muh. Zaky Raditya Nasywan:</b> Berasal dari Universitas Hasanuddin. Berperan merancang frontend aplikasi.</li>
        </ul>
    </div>
    <hr>
</div>