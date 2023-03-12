<script lang="ts">
    export let description:string;
    export let imageUrl:string;
    export let nickname:string;
    export let timeStamp:number;
    export let latency:number;
    function date2str(time:number){
        let date:Date = new Date(time);
        return date.toLocaleString();
    }
    function milisec2str(time:number){
        let date:Date = new Date(time);
        let day = date.getUTCDate()-1;
        let hour = date.getUTCHours();
        let min = date.getUTCMinutes();
        let sec = date.getUTCSeconds();
        return `${day}일 ${hour}시간 ${min}분 ${sec}초`;
    }
    
</script>
<div>
    <img src={imageUrl} alt="hi" height="200em"/>
    <p>{description}</p>
    <p>{nickname}</p>
    <p>{date2str(timeStamp)}</p>
    <p>소요시간: {milisec2str(latency)}</p>
</div>