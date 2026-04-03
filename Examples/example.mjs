import OpenAi from "openai";
const client = new OpenAi();

const response = await client.responses.create({
    model:"gpt-4o-mini",
    input: "Write a one-sentence bedime story about a unicorn."
});
console.log("--- 结构化数据 ---");
console.log(response.output_text);
console.log("--- 原始响应对象 ---");
console.log(response)