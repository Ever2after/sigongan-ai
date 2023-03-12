<script>
    // @ts-nocheck
        import Card from '../components/card.svelte';
        async function getData(){
            const res = await fetch('https://sigongan-3f44b-default-rtdb.firebaseio.com/archive.json');
            const json = await res.json();
            let arr = Object.entries(json).map(([key, value]) => value);
            return arr.sort((a, b) => - a.imageTimetamp + b.imageTimetamp);
        }
        let promise = getData();
        function click1(){
            promise = getData();
        }
        function averageLatency(array){
            let time = 0;
            array.forEach(el => {
                time += el.descTimestamp - el.imageTimetamp;
            });
            time = Math.round(time / array.length);
            return time;
        }
        function milisec2str(time){
            let date = new Date(time);
            let day = date.getUTCDate()-1;
            let hour = date.getUTCHours();
            let min = date.getUTCMinutes();
            let sec = date.getUTCSeconds();
            return `${day}일 ${hour}시간 ${min}분 ${sec}초`;
        }
    </script>
    <h1>시공간 해설 현황</h1>
    <button on:click={click1}>새로고침</button>
    {#await promise}
    <p>waiting...</p>
    {:then arr}
    <h2> 해설 횟수: {arr.length}</h2>
    <h2> 평균 소요 시간: {milisec2str(averageLatency(arr))}</h2>
    {#each arr as el}
    <Card description={el.description} timeStamp={el.imageTimetamp} nickname={el.nickname} imageUrl={el.imageUrl} latency={el.descTimestamp - el.imageTimetamp} />
    {/each}
    {/await}