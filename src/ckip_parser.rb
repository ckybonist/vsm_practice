#!/usr/bin/ruby

require 'json'
require_relative '../lib/ckip/CKIP_Client'

class NLTool
    def Segment(text)
        raw_corpus = CKIP.segment(text).split(" ")
        return raw_corpus
    end

    # 將 CKIP 分詞的結果做過濾，並轉換成我自己需要的格式
    def FilterCorpus(raw_corpus)
        raw_corpus.each do |term_of_sentence|
            term_of_sentence = term_of_sentence.split(" ")
        end
        corpus = raw_corpus.map { |sentence|
            sentence.gsub!(/\([^()]*\)/, "")
            sentence.gsub!(/[0-9\p{P}\=]/, "")  # 刪除詞性標記及標點符號
            sentence.delete!(" ")  #刪除空白
            full_width_space = [0x3000].pack('U')
            sentence.split(full_width_space)  # 依據全形空白切割字串
        }
        corpus = corpus.flat_map { |e| e }.reject! { |s| s.empty? }  # 合併子陣列，去掉空字串
        return corpus
    end

    def CountWords(corpus)
        freqs = Hash.new(0)
        corpus.each do |term|
            freqs[term] += 1
        end
        return Hash[freqs.sort_by { |t, f| f }]
    end
end

def GenrDocIndex()
    nl_tool = NLTool.new()
    doc_index = Hash.new()
    files = Dir.glob("../docs/*")

    files.each do |f|
        text = File.open(f, "r").read()
        raw_corpus = nl_tool.Segment(text)
        corpus = nl_tool.FilterCorpus(raw_corpus)
        doc_index[f] = corpus
    end

    File.open("../log/tmp_corpus.txt", "w") do |f|
        f.write(JSON.pretty_generate(doc_index))
    end
end


# Main Process
GenrDocIndex()

# End of File
